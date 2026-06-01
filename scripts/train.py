import argparse
import os
import sys

# Ensure repository root is on sys.path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app.model import train_model_pipeline
from app.utils import download_dataset_if_missing
from app.config import DATA_DIR, CLASS_NAMES

def main():
    parser = argparse.ArgumentParser(description='Train garbage classifier')
    parser.add_argument('--epochs', type=int, default=10)
    parser.add_argument('--dataset', type=str, default=DATA_DIR)
    parser.add_argument('--model', type=str, default=None)
    parser.add_argument('--dry-run', action='store_true', help='Only validate dataset and print counts')
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
        train_model_pipeline(args.dataset, epochs=args.epochs, model_path=args.model)
        try:
            print("Generating performance plot...")
            import subprocess
            subprocess.run([sys.executable, os.path.join(ROOT, 'scripts', 'plot_history.py')], check=True)
        except Exception as e:
            print(f"Warning: could not generate plot: {e}")

if __name__ == '__main__':
    main()