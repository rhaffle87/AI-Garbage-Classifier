"""Configuration Module.

Defines base directories, creates necessary local application folders,
specifies input dimensions, classification categories, and file paths
for saving trained model files (both modern .keras and legacy .h5 formats).
"""

import os

# =====================================================================
# Base Directory Declarations
# =====================================================================
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR = os.path.join(ROOT_DIR, 'data', 'garbage_classification')
MODELS_DIR = os.path.join(ROOT_DIR, 'models')
LOGS_DIR = os.path.join(ROOT_DIR, 'logs')

# Auto-create runtime directories if missing
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

# =====================================================================
# Model & Preprocessing Configuration Parameters
# =====================================================================
IMG_SIZE = (224, 224)  # MobileNetV2 standard shape: (height, width)
CLASS_NAMES = ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']
NUM_CLASSES = len(CLASS_NAMES)

# Model Storage File Paths
MODEL_PATH = os.path.join(MODELS_DIR, 'garbage_model.keras')  # Preferred TF format
PROD_MODEL_PATH = os.path.join(MODELS_DIR, 'garbage_model_prod.keras')  # Promoted production model
LEGACY_MODEL_PATH = os.path.join(MODELS_DIR, 'garbage_model.h5')  # Legacy format fallback

