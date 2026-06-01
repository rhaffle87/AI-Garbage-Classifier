"""Demo script: create sample data and train for 1 epoch to produce logs and a demo model."""
import os
from create_sample_data import CLASS_NAMES, DATA_DIR
from train import train

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
logs_dir = os.path.join(ROOT, 'logs', 'demo')
os.makedirs(logs_dir, exist_ok=True)
model_path = os.path.join(ROOT, 'models', 'demo_garbage_model.h5')

print('Creating sample data...')
# create_sample_data will have run if invoked directly; we call it here by running its module
import create_sample_data

print('Starting demo training (1 epoch)')
train(epochs=1, dataset_dir=DATA_DIR, model_path=model_path, logs_dir=logs_dir)
print('Demo training complete.')
print('Model:', model_path)
print('Logs:', logs_dir)
