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
    if dataset_dir.endswith('.tfrecords'):
        # -----------------------------------------------------------------
        # High-Performance TFRecord Ingestion Pipeline
        # -----------------------------------------------------------------
        import logging
        logging.info(f"Loading dataset from TFRecord path: {dataset_dir}")
        full_dataset = tf.data.TFRecordDataset(dataset_dir)
        
        # Determine total size dynamically (fallback to 2527 if slow/fails)
        try:
            total_images = sum(1 for _ in full_dataset)
        except Exception:
            total_images = 2527
            
        val_split = 0.2 if total_images >= 30 else 0.0
        val_size = int(total_images * val_split)
        train_size = total_images - val_size
        
        feature_description = {
            'image_raw': tf.io.FixedLenFeature([], tf.string),
            'label': tf.io.FixedLenFeature([], tf.int64)
        }
        
        def _parse_function(example_proto):
            features = tf.io.parse_single_example(example_proto, feature_description)
            image = tf.io.decode_jpeg(features['image_raw'], channels=3)
            image = tf.image.resize(image, IMG_SIZE)
            # Apply dynamic on-the-fly random horizontal flipping augmentations
            image = tf.image.random_flip_left_right(image)
            image = tf.cast(image, tf.float32) / 255.0
            label = features['label']
            return image, label

        parsed_dataset = full_dataset.map(_parse_function, num_parallel_calls=tf.data.AUTOTUNE)
        
        train_generator = parsed_dataset.take(train_size).shuffle(buffer_size=1000).batch(32).prefetch(tf.data.AUTOTUNE)
        if val_size > 0:
            validation_generator = parsed_dataset.skip(train_size).batch(32).prefetch(tf.data.AUTOTUNE)
        else:
            validation_generator = None
            
        if train_size == 0:
            logging.error('No training images found in TFRecord dataset.')
            raise RuntimeError('No training images found in TFRecord dataset')
    else:
        # -----------------------------------------------------------------
        # Standard Directory Ingestion Pipeline (Keras Generators)
        # -----------------------------------------------------------------
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

    from tensorflow.keras.callbacks import CSVLogger, EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
    import logging
    from app.config import LOGS_DIR
    
    csv_logger = CSVLogger(os.path.join(LOGS_DIR, 'training_history.csv'), append=True)
    
    class LoggingCallback(tf.keras.callbacks.Callback):
        def on_epoch_end(self, epoch, logs=None):
            logs = logs or {}
            logging.info(f"Epoch {epoch+1} - " + ", ".join([f"{k}={v:.4f}" for k, v in logs.items()]))
            
    logging_callback = LoggingCallback()

    checkpoint_path = model_path
    early_stopping = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True, verbose=1)
    model_checkpoint = ModelCheckpoint(filepath=checkpoint_path, monitor='val_accuracy', save_best_only=True, verbose=1)
    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=2, min_lr=1e-6, verbose=1)
    
    callbacks_list = [csv_logger, logging_callback, early_stopping, model_checkpoint, reduce_lr]

    # Optional Tracking & Governance hooks
    try:
        import wandb
        from wandb.integration.keras import WandbCallback
        if wandb.run is not None:
            callbacks_list.append(WandbCallback(save_model=False))
            logging.info("Weights & Biases callback attached.")
    except ImportError:
        pass

    try:
        import mlflow
        import mlflow.keras
        mlflow.keras.autolog()
        logging.info("MLflow autologging enabled.")
    except ImportError:
        pass

    history = model.fit(
        train_generator,
        validation_data=validation_generator,
        epochs=epochs,
        callbacks=callbacks_list
    )

    # =====================================================================
    # Stage 2: Fine-Tuning deep MobileNetV2 layers
    # =====================================================================
    import logging
    logging.info("Initiating Stage 2: Fine-tuning base MobileNetV2 layers...")
    print("\n--- Starting Stage 2: Fine-Tuning Base MobileNetV2 Layers ---")
    
    base_model.trainable = True
    # Freeze the early feature extractor layers, leaving deep layers (100+) trainable
    for layer in base_model.layers[:100]:
        layer.trainable = False
        
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    fine_tune_epochs = max(2, epochs // 2)
    history_fine = model.fit(
        train_generator,
        validation_data=validation_generator,
        epochs=fine_tune_epochs,
        callbacks=callbacks_list
    )

    # Restore best checkpointed model weights if saved
    if os.path.exists(checkpoint_path):
        try:
            model = tf.keras.models.load_model(checkpoint_path)
            logging.info("Loaded best model weights from checkpoint.")
        except Exception as e:
            logging.warning(f"Could not load best model checkpoint, using final weights: {e}")

    model.save(model_path)
    import logging
    logging.info(f"Model saved to {model_path}")
    print(f"[SUCCESS] Model successfully saved to {model_path}")
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