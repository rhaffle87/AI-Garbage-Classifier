import os
import shutil

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
ARCHIVE_DIR = os.path.join(ROOT_DIR, 'archive')
NESTED_DATASET_DIR = os.path.join(ARCHIVE_DIR, 'Garbage classification', 'Garbage classification')
DATA_DIR = os.path.join(ROOT_DIR, 'data', 'garbage_classification')

CLASS_NAMES = ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']

def reorganize():
    print(f"Reorganizing dataset structure...")
    print(f"Root: {ROOT_DIR}")
    print(f"Nested source: {NESTED_DATASET_DIR}")
    print(f"Archive target: {ARCHIVE_DIR}")
    print(f"Data target: {DATA_DIR}")

    # Check if nested source folder exists
    if not os.path.exists(NESTED_DATASET_DIR):
        print(f"Nested folder not found at {NESTED_DATASET_DIR}. Checking if already reorganized...")
        # Check if directories exist directly in archive
        direct_exists = all(os.path.exists(os.path.join(ARCHIVE_DIR, cls)) for cls in CLASS_NAMES)
        if direct_exists:
            print("Categories already directly in archive. Let's make sure they are in data/ as well.")
        else:
            print("Error: Could not locate nested dataset or reorganized category folders.")
            return False
    else:
        # Move folders from NESTED_DATASET_DIR to ARCHIVE_DIR
        for cls in CLASS_NAMES:
            src_cls_dir = os.path.join(NESTED_DATASET_DIR, cls)
            dst_cls_dir = os.path.join(ARCHIVE_DIR, cls)

            if os.path.exists(src_cls_dir):
                if os.path.exists(dst_cls_dir):
                    print(f"Destination {dst_cls_dir} already exists. Merging files...")
                    for file_name in os.listdir(src_cls_dir):
                        src_file = os.path.join(src_cls_dir, file_name)
                        dst_file = os.path.join(dst_cls_dir, file_name)
                        if os.path.isfile(src_file) and not os.path.exists(dst_file):
                            shutil.move(src_file, dst_file)
                else:
                    print(f"Moving {src_cls_dir} -> {dst_cls_dir}")
                    shutil.move(src_cls_dir, dst_cls_dir)
            else:
                print(f"Warning: Category folder {src_cls_dir} not found.")

        # Clean up empty source directories
        nested_parent = os.path.join(ARCHIVE_DIR, 'Garbage classification')
        try:
            print(f"Removing nested directories in {nested_parent}...")
            shutil.rmtree(nested_parent)
            print(f"Successfully cleaned up empty nested archive directories.")
        except Exception as e:
            print(f"Error cleaning up nested directories: {e}")

    # Copy files from ARCHIVE_DIR to DATA_DIR to populate active training dataset
    for cls in CLASS_NAMES:
        archive_cls_dir = os.path.join(ARCHIVE_DIR, cls)
        active_cls_dir = os.path.join(DATA_DIR, cls)

        if os.path.exists(archive_cls_dir):
            print(f"Populating active dataset for class '{cls}'...")
            # If the active directory exists, clear any old placeholder files
            if os.path.exists(active_cls_dir):
                shutil.rmtree(active_cls_dir)
            os.makedirs(active_cls_dir, exist_ok=True)

            # Copy files
            cnt = 0
            for file_name in os.listdir(archive_cls_dir):
                src_file = os.path.join(archive_cls_dir, file_name)
                dst_file = os.path.join(active_cls_dir, file_name)
                if os.path.isfile(src_file) and file_name.lower().endswith(('.jpg', '.jpeg', '.png')):
                    shutil.copy2(src_file, dst_file)
                    cnt += 1
            print(f"  Copied {cnt} images for '{cls}' to active dataset.")
        else:
            print(f"Error: Reorganized folder {archive_cls_dir} does not exist.")

    print("\n[OK] Reorganization & Dataset integration complete!")
    return True

if __name__ == '__main__':
    reorganize()
