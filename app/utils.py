"""Utilities Module.

Provides data acquisition wrappers, image file loaders, custom dataset
preprocessing routines, and inference vector formatting logic.
"""

import os
import shutil
import cv2
import numpy as np
from app.config import IMG_SIZE, DATA_DIR, CLASS_NAMES

def download_dataset_if_missing():
    """Verifies presence of local training data.

    Checks active project data folders. If missing, attempts to populate from local
    unpacked dataset archives. If archive folders are not found, fallback to pulling
    and unpacking remote datasets from Kaggle.
    """
    missing = False
    for c in CLASS_NAMES:
        c_dir = os.path.join(DATA_DIR, c)
        if not os.path.exists(c_dir) or len(os.listdir(c_dir)) == 0:
            missing = True
            break
            
    if missing:
        # Check if we have the local archive folders as an alternative to downloading
        ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        archive_dir = os.path.join(ROOT_DIR, 'archive')
        local_archive_exists = True
        for c in CLASS_NAMES:
            c_archive = os.path.join(archive_dir, c)
            if not os.path.exists(c_archive) or len(os.listdir(c_archive)) == 0:
                local_archive_exists = False
                break
        
        if local_archive_exists:
            print("Found local archive folders. Copying to active dataset...")
            for c in CLASS_NAMES:
                src_dir = os.path.join(archive_dir, c)
                dst_dir = os.path.join(DATA_DIR, c)
                if os.path.exists(dst_dir):
                    shutil.rmtree(dst_dir)
                os.makedirs(dst_dir, exist_ok=True)
                for f in os.listdir(src_dir):
                    if f.lower().endswith(('.png', '.jpg', '.jpeg')):
                        shutil.copy2(os.path.join(src_dir, f), os.path.join(dst_dir, f))
            print("Dataset populated from local archive.")
        else:
            import kagglehub
            print("Downloading dataset from Kaggle...")
            path = kagglehub.dataset_download("asdasdasasdas/garbage-classification")
            print(f"Downloaded to {path}. Moving to {DATA_DIR}...")
            
            for root, dirs, files in os.walk(path):
                for d in dirs:
                    if d.lower() in [c.lower() for c in CLASS_NAMES]:
                        src_dir = os.path.join(root, d)
                        # Use the correct canonical name from CLASS_NAMES
                        target_class = next(c for c in CLASS_NAMES if c.lower() == d.lower())
                        dst_dir = os.path.join(DATA_DIR, target_class)
                        os.makedirs(dst_dir, exist_ok=True)
                        for f in os.listdir(src_dir):
                            if f.lower().endswith(('.png', '.jpg', '.jpeg')):
                                shutil.copy2(os.path.join(src_dir, f), os.path.join(dst_dir, f))
            print("Dataset ready.")
    else:
        print("Dataset already exists locally.")

def load_and_preprocess_image(image_path, target_size=None):
    """Loads an image from the specified path, resizes it, and normalizes pixel values.

    Args:
        image_path (str): Absolute file path to the image.
        target_size (tuple, optional): Target (height, width) dimensions. Defaults to IMG_SIZE.

    Returns:
        np.ndarray: The preprocessed image array normalized to [0, 1], or None if load fails.
    """
    if target_size is None:
        target_size = IMG_SIZE
    
    img = cv2.imread(image_path)
    if img is None:
        return None
        
    # Performance Optimization: Skip resizing if image dimensions already match target
    if img.shape[0] != target_size[0] or img.shape[1] != target_size[1]:
        img = cv2.resize(img, target_size)
        
    img = img / 255.0  # Normalize pixel values
    return img

def load_data(dataset_path, target_size=None):
    """Loads and preprocesses all images and labels from the dataset directory.

    Checks for missing directories and populates the dataset locally or remotely
    before loading.

    Args:
        dataset_path (str): Path to the dataset root folder.
        target_size (tuple, optional): Target (height, width) dimensions. Defaults to IMG_SIZE.

    Returns:
        tuple: (images_array, labels_array, CLASS_NAMES)
    """
    download_dataset_if_missing()
    images = []
    labels = []

    for label in CLASS_NAMES:
        label_path = os.path.join(dataset_path, label)
        if os.path.isdir(label_path):
            for img_file in os.listdir(label_path):
                img_path = os.path.join(label_path, img_file)
                if img_file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    img = load_and_preprocess_image(img_path, target_size=target_size)
                    if img is not None:
                        images.append(img)
                        labels.append(CLASS_NAMES.index(label))

    return np.array(images), np.array(labels), CLASS_NAMES


def preprocess_image(image, target_size=None):
    """Preprocesses a PIL Image or numpy array to model input shape.

    Args:
        image (PIL.Image.Image or np.ndarray): Raw input image.
        target_size (tuple, optional): Target (height, width) dimensions. Defaults to IMG_SIZE.

    Returns:
        np.ndarray: Normalized image array matching target_size.

    Raises:
        ValueError: If the input image format is unsupported.
    """
    if target_size is None:
        target_size = IMG_SIZE

    try:
        from PIL import Image
        if isinstance(image, Image.Image):
            image = image.convert('RGB')
            image = np.array(image)
    except Exception:
        pass

    if isinstance(image, np.ndarray):
        if image.ndim == 3 and image.shape[2] == 3:
            # Performance Optimization: Skip resizing if dimensions already match target
            if image.shape[0] != target_size[0] or image.shape[1] != target_size[1]:
                img = cv2.resize(image, target_size)
            else:
                img = image
            img = img.astype('float32') / 255.0
            return img

    raise ValueError('Unsupported image format for preprocessing')


def write_tfrecords(dataset_path, output_tfrecord_path):
    """Converts a directory-structured image dataset into a serialized TFRecord file.

    Args:
        dataset_path (str): Root folder containing class directories.
        output_tfrecord_path (str): Target output file path.
    """
    import tensorflow as tf
    
    def _bytes_feature(value):
        return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

    def _int64_feature(value):
        return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))

    writer = tf.io.TFRecordWriter(output_tfrecord_path)
    for label in CLASS_NAMES:
        label_dir = os.path.join(dataset_path, label)
        if not os.path.exists(label_dir):
            continue
        label_idx = CLASS_NAMES.index(label)
        for filename in os.listdir(label_dir):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                img_path = os.path.join(label_dir, filename)
                try:
                    with open(img_path, 'rb') as f:
                        img_bytes = f.read()
                    feature = {
                        'image_raw': _bytes_feature(img_bytes),
                        'label': _int64_feature(label_idx)
                    }
                    example = tf.train.Example(features=tf.train.Features(feature=feature))
                    writer.write(example.SerializeToString())
                except Exception as e:
                    print(f"Warning: failed to serialize {img_path}: {e}")
    writer.close()


def load_tfrecord_dataset(tfrecord_path, batch_size=32, target_size=None):
    """Loads and decodes a TFRecord dataset into a tf.data.Dataset ready for training.

    Args:
        tfrecord_path (str): Path to the TFRecord file.
        batch_size (int): Batch size.
        target_size (tuple, optional): Target (height, width) dimensions. Defaults to IMG_SIZE.

    Returns:
        tf.data.Dataset: Preprocessed and batched dataset.
    """
    import tensorflow as tf
    if target_size is None:
        target_size = IMG_SIZE

    feature_description = {
        'image_raw': tf.io.FixedLenFeature([], tf.string),
        'label': tf.io.FixedLenFeature([], tf.int64)
    }

    def _parse_function(example_proto):
        features = tf.io.parse_single_example(example_proto, feature_description)
        image = tf.io.decode_jpeg(features['image_raw'], channels=3)
        image = tf.image.resize(image, target_size)
        image = tf.cast(image, tf.float32) / 255.0
        label = features['label']
        return image, label

    dataset = tf.data.TFRecordDataset(tfrecord_path)
    dataset = dataset.map(_parse_function, num_parallel_calls=tf.data.AUTOTUNE)
    dataset = dataset.shuffle(buffer_size=1000)
    dataset = dataset.batch(batch_size)
    dataset = dataset.prefetch(buffer_size=tf.data.AUTOTUNE)
    return dataset