import argparse
import os
import sys
import tensorflow as tf

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app.config import MODEL_PATH


def export_tflite(model_path=MODEL_PATH, output_path=None):
    """Converts a trained Keras model to TensorFlow Lite format."""
    if not os.path.exists(model_path):
        print(f"Error: Target model not found at {model_path}")
        return False

    if output_path is None:
        output_path = model_path.replace(".h5", ".tflite").replace(".keras", ".tflite")

    print(f"Loading model from {model_path}...")
    try:
        model = tf.keras.models.load_model(model_path)
    except Exception as e:
        print(f"Failed to load model: {e}")
        return False

    print("Converting to TensorFlow Lite...")
    converter = tf.lite.TFLiteConverter.from_keras_model(model)

    # Optional optimizations
    converter.optimizations = [tf.lite.Optimize.DEFAULT]

    tflite_model = converter.convert()

    with open(output_path, "wb") as f:
        f.write(tflite_model)

    print(f"[SUCCESS] Exported TFLite model to {output_path}")
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export Keras model to TFLite format")
    parser.add_argument(
        "--model", type=str, default=MODEL_PATH, help="Input model path"
    )
    parser.add_argument("--output", type=str, default=None, help="Output TFLite path")
    args = parser.parse_args()

    export_tflite(args.model, args.output)
