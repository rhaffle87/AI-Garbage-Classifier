"""Create a tiny sample dataset for the garbage classifier.
Creates 3 simple synthetic images per class under data/garbage_classification.
"""
from PIL import Image, ImageDraw, ImageFont
import os

CLASS_NAMES = ['cardboard','glass','metal','paper','plastic','trash']
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR = os.path.join(ROOT, 'data', 'garbage_classification')

os.makedirs(DATA_DIR, exist_ok=True)

print(f"Creating sample dataset in {DATA_DIR}")
for cls in CLASS_NAMES:
    cls_dir = os.path.join(DATA_DIR, cls)
    # If a file exists with the same name as the intended directory (e.g., a README
    # placeholder), rename it safely before creating the directory so we don't
    # raise on Windows when trying to make the directory.
    if os.path.exists(cls_dir) and os.path.isfile(cls_dir):
        new_name = cls_dir + '.txt'
        print(f"Warning: found file at {cls_dir}; renaming to {new_name} to create directory")
        os.rename(cls_dir, new_name)
    os.makedirs(cls_dir, exist_ok=True)
    for i in range(1,4):
        # Create a simple colored image
        # Use a deterministic-ish color based on class name + index
        color_seed = f"{cls}{i}"
        img = Image.new('RGB', (128,128), color=(int(hash(color_seed) & 255), (i*60)%256, (i*120)%256))
        draw = ImageDraw.Draw(img)
        draw.rectangle([10,10,118,118], outline=(255,255,255), width=2)
        draw.text((12,12), f"{cls[:6]}-{i}", fill=(255,255,255))
        path = os.path.join(cls_dir, f"{cls}_{i}.jpg")
        img.save(path, 'JPEG')
        print(f"  wrote {path}")

print('Sample dataset created.')
