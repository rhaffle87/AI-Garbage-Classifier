import argparse
import os
import sys

# Ensure repository root is on sys.path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app.model import train_model_pipeline
from app.utils import download_dataset_if_missing, write_tfrecords
from app.config import DATA_DIR, CLASS_NAMES

def main():
    parser = argparse.ArgumentParser(description='Train garbage classifier with enterprise pipeline')
    parser.add_argument('--epochs', type=int, default=10)
    parser.add_argument('--dataset', type=str, default=DATA_DIR)
    parser.add_argument('--model', type=str, default=None)
    parser.add_argument('--dry-run', action='store_true', help='Only validate dataset and print counts')
    parser.add_argument('--tfrecords', action='store_true', help='Serialize dataset to TFRecords for high-performance training')
    parser.add_argument('--wandb', type=str, default=None, help='Weights & Biases project name to log metrics')
    parser.add_argument('--mlflow', action='store_true', help='Enable MLflow run tracking')
    args = parser.parse_args()

    if not args.dry_run:
        download_dataset_if_missing()

    if args.dry_run:
        print(f"Dry run: found {len(CLASS_NAMES)} classes.")
        for label in CLASS_NAMES:
            label_path = os.path.join(args.dataset, label)
            if os.path.exists(label_path):
                cnt = len([f for f in os.listdir(label_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
                print(f"- {label}: {cnt}")
            else:
                print(f"- {label}: 0 (directory missing)")
    else:
        # Initialize W&B if enabled
        if args.wandb:
            try:
                import wandb
                wandb.init(project=args.wandb, config={
                    "epochs": args.epochs,
                    "use_tfrecords": args.tfrecords,
                    "architecture": "MobileNetV2"
                })
                print(f"[W&B] Initialized W&B project: {args.wandb}")
            except ImportError:
                print("[W&B] Warning: wandb library not installed. Skipping W&B initialization.")

        # Initialize MLflow if enabled
        if args.mlflow:
            try:
                import mlflow
                mlflow.set_experiment("garbage-classifier")
                mlflow.start_run()
                mlflow.log_param("epochs", args.epochs)
                mlflow.log_param("use_tfrecords", args.tfrecords)
                print("[MLflow] Initialized experiment: garbage-classifier")
            except ImportError:
                print("[MLflow] Warning: mlflow library not installed. Skipping MLflow run.")

        training_data_source = args.dataset
        if args.tfrecords:
            tfrecord_file = os.path.join(ROOT, 'data', 'garbage_dataset.tfrecords')
            print(f"[TFRecords] Converting dataset {args.dataset} to TFRecord format...")
            write_tfrecords(args.dataset, tfrecord_file)
            print(f"[TFRecords] Successfully serialized to {tfrecord_file}")
            training_data_source = tfrecord_file

        print(f"Starting training pipeline on source: {training_data_source} for {args.epochs} epochs.")
        train_model_pipeline(training_data_source, epochs=args.epochs, model_path=args.model)

        # End active runs if applicable
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

        try:
            print("Generating performance plot...")
            import subprocess
            subprocess.run([sys.executable, os.path.join(ROOT, 'scripts', 'plot_history.py')], check=True)
        except Exception as e:
            print(f"Warning: could not generate plot: {e}")

if __name__ == '__main__':
    main()