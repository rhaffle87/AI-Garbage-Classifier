"""Model Architecture and Pipeline Module.

Handles loading trained classifier checkpoints, compiling model topologies,
training model parameters via Transfer Learning (MobileNetV2), running inference
predictions, and exposing classification tags.
"""

import os
import numpy as np
from tensorflow.keras.models import load_model as keras_load_model
from app.config import IMG_SIZE, NUM_CLASSES, MODEL_PATH, LEGACY_MODEL_PATH, CLASS_NAMES

def load_model(model_path=None):
    """Loads a pre-trained Keras/TensorFlow classification model.

    If the requested model file is missing, falls back to loading a legacy
    checkpoint path, or creates and compiles a lightweight fallback architecture.

    Args:
        model_path (str, optional): Target file path to .keras or .h5 file. Defaults to MODEL_PATH.

    Returns:
        tf.keras.Model: The compiled Keras model object.
    """
    if model_path is None:
        model_path = MODEL_PATH
    try:
        if os.path.exists(model_path):
            m = keras_load_model(model_path)
        elif os.path.exists(LEGACY_MODEL_PATH):
            m = keras_load_model(LEGACY_MODEL_PATH)
        else:
            raise FileNotFoundError("Model file not found")
        m._is_fallback = False
        return m
    except Exception as e:
        import warnings
        warnings.warn(f"Could not load model: {e}. Using a fallback untrained model.")
        from tensorflow.keras import layers, models
        fallback = models.Sequential([
            layers.Input(shape=(IMG_SIZE[0], IMG_SIZE[1], 3)),
            layers.Conv2D(8, (3, 3), activation='relu'),
            layers.MaxPooling2D((2, 2)),
            layers.Flatten(),
            layers.Dense(16, activation='relu'),
            layers.Dense(NUM_CLASSES, activation='softmax')
        ])
        fallback.compile(optimizer='adam', loss='sparse_categorical_crossentropy')
        fallback._is_fallback = True
        return fallback

def train_model_pipeline(dataset_dir, epochs=10, model_path=None):
    """Executes the full image classification training pipeline.

    Loads the dataset, configures image data generators with data augmentation
    properties, configures a MobileNetV2 base network pre-trained on ImageNet with
    weights frozen, attaches classification heads, trains the network, and writes
    history metrics and model binaries to disk.

    Args:
        dataset_dir (str): Folder path containing category subdirectories.
        epochs (int, optional): Total training iterations. Defaults to 10.
        model_path (str, optional): Target file path to write trained binaries. Defaults to MODEL_PATH.

    Returns:
        tuple: (trained_tf_keras_Model, history_object)
    """
    if model_path is None:
        model_path = MODEL_PATH
        
    import tensorflow as tf
    from tensorflow.keras.preprocessing.image import ImageDataGenerator
    from tensorflow.keras.applications import MobileNetV2
    from tensorflow.keras import layers, models

    import os
    total_images = sum([1 for r, d, files in os.walk(dataset_dir) for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
    val_split = 0.2 if total_images >= 30 else 0.0

    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        validation_split=val_split
    )

    train_generator = train_datagen.flow_from_directory(
        dataset_dir,
        target_size=IMG_SIZE,
        batch_size=32,
        class_mode='sparse',
        subset='training',
        shuffle=True
    )

    if val_split > 0:
        validation_generator = train_datagen.flow_from_directory(
            dataset_dir,
            target_size=IMG_SIZE,
            batch_size=32,
            class_mode='sparse',
            subset='validation'
        )
    else:
        validation_generator = None

    if train_generator.samples == 0:
        import logging
        logging.error('No training images found. Aborting training.')
        raise RuntimeError('No training images found in dataset directory')

    base_model = MobileNetV2(
        input_shape=(IMG_SIZE[0], IMG_SIZE[1], 3),
        include_top=False,
        weights='imagenet'
    )
    base_model.trainable = False

    model = models.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.2),
        layers.Dense(NUM_CLASSES, activation='softmax')
    ])

    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    from tensorflow.keras.callbacks import CSVLogger
    import logging
    from app.config import LOGS_DIR
    
    csv_logger = CSVLogger(os.path.join(LOGS_DIR, 'training_history.csv'), append=True)
    
    class LoggingCallback(tf.keras.callbacks.Callback):
        def on_epoch_end(self, epoch, logs=None):
            logs = logs or {}
            logging.info(f"Epoch {epoch+1} - " + ", ".join([f"{k}={v:.4f}" for k, v in logs.items()]))
            
    logging_callback = LoggingCallback()

    history = model.fit(
        train_generator,
        validation_data=validation_generator,
        epochs=epochs,
        callbacks=[csv_logger, logging_callback]
    )

    model.save(model_path)
    import logging
    logging.info(f"Model saved to {model_path}")
    print(f"✅ Model successfully saved to {model_path}")
    return model, history

def predict(model, image):
    """Executes inference on a single image.

    Inspects the model input layer properties to dynamically resize the input image,
    normalizes it, feeds it to the model, and outputs the raw softmax category probabilities.

    Args:
        model (tf.keras.Model): Loaded classification model.
        image (str or np.ndarray or PIL.Image.Image): File path or image array to classify.

    Returns:
        list: Softmax probability scores matching indices of CLASS_NAMES.
    """
    from app.utils import preprocess_image
    
    # Determine the model's expected input dimensions dynamically
    try:
        if isinstance(model.input_shape, list):
            shape = model.input_shape[0]
        else:
            shape = model.input_shape
        # shape format is (None, height, width, channels)
        h, w = shape[1], shape[2]
        if h is None or w is None:
            from app.config import IMG_SIZE
            target_size = IMG_SIZE
        else:
            target_size = (h, w)
    except Exception:
        from app.config import IMG_SIZE
        target_size = IMG_SIZE

    if isinstance(image, str):
        import cv2
        img = cv2.imread(image)
        if img is None:
            raise ValueError(f"Could not load image from path: {image}")
        processed = preprocess_image(img, target_size=target_size)
    else:
        processed = preprocess_image(image, target_size=target_size)

    input_batch = np.expand_dims(processed, axis=0)
    preds = model.predict(input_batch)
    return preds.tolist()[0]

def get_class_names():
    """Exposes the canonical sorted classification categories.

    Returns:
        list: List of category string labels.
    """
    return CLASS_NAMES