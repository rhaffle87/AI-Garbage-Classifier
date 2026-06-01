import os
import sys
import numpy as np

# Ensure repository root is on sys.path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from sklearn.metrics import classification_report, confusion_matrix
from app.model import load_model
from app.utils import load_data
from app.config import CLASS_NAMES, DATA_DIR, IMG_SIZE

def evaluate_model(test_data_path=DATA_DIR, model_path=None):
    """Loads a trained model and evaluates it on the test dataset.

    Args:
        test_data_path (str): Path to the evaluation dataset folder.
        model_path (str, optional): Custom model file path to load.

    Returns:
        tuple: (classification_report_dict, confusion_matrix_ndarray)
    """
    model = load_model(model_path)

    
    # Determine the model's expected input dimensions dynamically
    try:
        if isinstance(model.input_shape, list):
            shape = model.input_shape[0]
        else:
            shape = model.input_shape
        # shape is (None, height, width, channels)
        h, w = shape[1], shape[2]
        if h is None or w is None:
            target_size = IMG_SIZE
        else:
            target_size = (h, w)
    except Exception:
        target_size = IMG_SIZE

    X_test, y_test, _ = load_data(test_data_path, target_size=target_size)

    if len(X_test) == 0:
        raise ValueError("No images found for evaluation.")

    # Make predictions
    y_pred = model.predict(X_test)
    y_pred_classes = np.argmax(y_pred, axis=1)

    # Generate metrics
    report = classification_report(y_test, y_pred_classes, target_names=CLASS_NAMES, output_dict=True)
    cm = confusion_matrix(y_test, y_pred_classes)
    
    return report, cm

if __name__ == "__main__":
    report, cm = evaluate_model()
    print("Classification Report:")
    print(report)
    print("Confusion Matrix:")
    print(cm)