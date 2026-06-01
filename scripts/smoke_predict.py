import sys
import os
# Ensure repo root is on the path so `app` can be imported when running the script
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.model import load_model, predict, get_class_names
from PIL import Image

if __name__ == '__main__':
    model = load_model()
    img_path = 'data/garbage_classification/cardboard/cardboard_1.jpg'
    img = Image.open(img_path)
    probs = predict(model, img)
    classes = get_class_names()
    top = sorted(zip(classes, probs), key=lambda x: x[1], reverse=True)[:3]
    print('Image:', img_path)
    print('Top-3 predictions:')
    for cls, p in top:
        print(f'  {cls}: {p:.4f}')
