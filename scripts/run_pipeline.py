import os
import sys
import time
import argparse
from datetime import datetime

# Ensure repository root is on sys.path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app.utils import download_dataset_if_missing, write_tfrecords
from app.config import DATA_DIR, MODELS_DIR, LOGS_DIR, CLASS_NAMES
from scripts.evaluate import evaluate_model

def run_data_validation():
    """Runs data quality and validation checks on the dataset directory."""
    print("--- [Stage 1/6] Running Data Validation & Quality Checks ---")
    if not os.path.exists(DATA_DIR):
        print(f"[Validation Error] Data directory {DATA_DIR} does not exist.")
        return False
    
    classes_found = os.listdir(DATA_DIR)
    missing_classes = [c for c in CLASS_NAMES if c not in classes_found]
    if missing_classes:
        print(f"[Validation Warning] Missing expected class directories: {missing_classes}")
    
    valid = True
    total_images = 0
    for label in CLASS_NAMES:
        class_path = os.path.join(DATA_DIR, label)
        if not os.path.exists(class_path):
            print(f"[Validation Error] Directory for class '{label}' is missing.")
            valid = False
            continue
        
        files = [f for f in os.listdir(class_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        print(f"  - Class '{label}': {len(files)} images found.")
        total_images += len(files)
        if len(files) == 0:
            print(f"[Validation Error] Class '{label}' has 0 valid images.")
            valid = False
            
    if total_images < 100:
        print(f"[Validation Error] Total dataset size ({total_images} images) is too small for robust training.")
        valid = False
        
    if valid:
        print(f"[Validation Success] Dataset validated: {total_images} total images across {len(CLASS_NAMES)} classes.\n")
    else:
        print("[Validation Failed] Data quality checks failed. See errors above.\n")
    return valid

def serialize_dataset():
    """Converts the raw image directory into serialized TFRecords for high-performance streaming."""
    print("--- [Stage 2/6] Converting Dataset to Serialized TFRecords ---")
    tfrecord_file = os.path.join(ROOT, 'data', 'garbage_dataset.tfrecords')
    try:
        write_tfrecords(DATA_DIR, tfrecord_file)
        print(f"[TFRecords Success] Serialized TFRecord dataset created at: {tfrecord_file}\n")
        return tfrecord_file
    except Exception as e:
        print(f"[TFRecords Error] Failed to serialize dataset: {e}\n")
        return None

def train_model(epochs, use_tfrecords, tfrecord_file):
    """Executes model training using train_model_pipeline."""
    print("--- [Stage 3/6] Running Transfer Learning & Fine-Tuning Pipeline ---")
    from app.model import train_model_pipeline
    
    source = tfrecord_file if use_tfrecords else DATA_DIR
    print(f"Training model on source: {source} for {epochs} epochs.")
    
    try:
        train_model_pipeline(source, epochs=epochs)
        print("[Training Success] Model trained and checkpointed successfully.\n")
        return True
    except Exception as e:
        print(f"[Training Error] Model training failed: {e}\n")
        return False

def evaluate_and_promote(min_accuracy_threshold=0.75):
    """Runs model evaluation sweep, promos checkpoint if accuracy meets quality gate."""
    print("--- [Stage 4/6] Running Model Evaluation Sweep ---")
    checkpoint_path = os.path.join(MODELS_DIR, 'garbage_model.keras')
    try:
        report, cm = evaluate_model(model_path=checkpoint_path)

        acc = report.get('accuracy', 0.0)
        macro_f1 = report.get('macro avg', {}).get('f1-score', 0.0)
        
        print(f"Evaluation Metrics:")
        print(f"  - Test Accuracy: {acc:.4f} (Required: >= {min_accuracy_threshold:.4f})")
        print(f"  - Macro F1-Score: {macro_f1:.4f}")
        
        print("\n--- [Stage 5/6] Model Promotion Quality Gate Decision ---")
        promoted = False
        if acc >= min_accuracy_threshold:
            print(f"[Promotion Success] Test accuracy {acc:.4f} satisfies quality gate threshold of {min_accuracy_threshold:.4f}.")
            prod_model_path = os.path.join(MODELS_DIR, 'garbage_model_prod.keras')
            import shutil
            shutil.copyfile(
                os.path.join(MODELS_DIR, 'garbage_model.keras'),
                prod_model_path
            )
            print(f"[Promotion Promoted] Model copied to active production endpoint: {prod_model_path}")
            promoted = True
        else:
            print(f"[Promotion Rejected] Test accuracy {acc:.4f} did not meet quality gate threshold of {min_accuracy_threshold:.4f}. Model will not be promoted.")
            
        return report, cm, promoted
    except Exception as e:
        print(f"[Evaluation Error] Evaluation or promotion decision failed: {e}\n")
        return None, None, False

def log_pipeline_summary(metrics, promoted, epochs, use_tfrecords, duration_sec):
    """Writes a Markdown summary log of the pipeline run to logs/pipeline_run_summary.md."""
    print("--- [Stage 6/6] Logging Pipeline Summary & Observability Reports ---")
    summary_path = os.path.join(LOGS_DIR, 'pipeline_run_summary.md')
    
    acc = metrics.get('accuracy', 0.0) if metrics else 0.0
    macro_f1 = metrics.get('macro avg', {}).get('f1-score', 0.0) if metrics else 0.0
    
    summary_md = f"""# MLOps Pipeline Run Summary
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Duration: {duration_sec:.2f} seconds

## Configuration
- Epochs: {epochs}
- Streaming Format: {"TFRecords" if use_tfrecords else "Raw Directory"}
- Quality Gate Threshold: 75.00%

## Execution Results
- Data Quality Validation: PASS
- Model Training status: SUCCESS
- Model Evaluation status: SUCCESS

## Evaluation Metrics
- **Test Accuracy**: {acc * 100:.2f}%
- **Macro F1-Score**: {macro_f1 * 100:.2f}%

## Promotion Decision
- **Promoted to Production**: {"✅ YES" if promoted else "❌ NO"}
"""
    try:
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(summary_md)
        print(f"[Summary Success] Report generated at: {summary_path}\n")
        
        # Log to MLflow if active
        try:
            import mlflow
            if mlflow.active_run():
                mlflow.log_metric("pipeline_test_accuracy", acc)
                mlflow.log_metric("pipeline_macro_f1", macro_f1)
                mlflow.log_param("pipeline_promoted", promoted)
                print("[MLflow] Successfully logged pipeline metrics to active MLflow run.")
        except Exception:
            pass
            
    except Exception as e:
        print(f"[Summary Error] Failed to write run summary: {e}\n")

def main():
    parser = argparse.ArgumentParser(description="End-to-end MLOps pipeline for AI Garbage Classifier")
    parser.add_argument('--epochs', type=int, default=5, help="Number of training epochs")
    parser.add_argument('--no-tfrecords', action='store_true', help="Disable TFRecord streaming and train on raw directories")
    parser.add_argument('--threshold', type=float, default=0.75, help="Quality gate accuracy threshold for model promotion")
    parser.add_argument('--wandb', type=str, default=None, help="Weights & Biases project name")
    parser.add_argument('--mlflow', action='store_true', help="Enable MLflow observability logging")
    args = parser.parse_args()
    
    start_time = time.time()
    
    # 1. Download/Verify Data
    download_dataset_if_missing()
    
    # 2. Validate Data Quality
    if not run_data_validation():
        sys.exit(1)
        
    # 3. Serialize to TFRecords if requested
    use_tfrecords = not args.no_tfrecords
    tfrecord_file = None
    if use_tfrecords:
        tfrecord_file = serialize_dataset()
        if not tfrecord_file:
            print("[Pipeline Aborted] TFRecord serialization failed.")
            sys.exit(1)
            
    # Setup MLflow / W&B globally if requested
    if args.wandb:
        try:
            import wandb
            wandb.init(project=args.wandb, config={
                "epochs": args.epochs,
                "use_tfrecords": use_tfrecords,
                "architecture": "MobileNetV2"
            })
        except ImportError:
            pass

    if args.mlflow:
        try:
            import mlflow
            mlflow.set_experiment("garbage-classifier-pipeline")
            mlflow.start_run()
            mlflow.log_param("pipeline_epochs", args.epochs)
            mlflow.log_param("pipeline_tfrecords", use_tfrecords)
        except ImportError:
            pass
            
    # 4. Train Model
    train_success = train_model(args.epochs, use_tfrecords, tfrecord_file)
    if not train_success:
        print("[Pipeline Aborted] Model training failed.")
        sys.exit(1)
        
    # 5. Evaluate and Promote model
    metrics, cm, promoted = evaluate_and_promote(args.threshold)
    
    duration = time.time() - start_time
    
    # 6. Log Pipeline Summary
    log_pipeline_summary(metrics, promoted, args.epochs, use_tfrecords, duration)
    
    # Close W&B / MLflow
    if args.wandb:
        try:
            import wandb
            if wandb.run:
                wandb.finish()
        except ImportError:
            pass
    if args.mlflow:
        try:
            import mlflow
            if mlflow.active_run():
                mlflow.end_run()
        except ImportError:
            pass
            
    print(f"[Pipeline Complete] Finished in {duration:.2f} seconds.")

if __name__ == '__main__':
    main()
