import os
import io
import base64
from typing import Dict, Any
from functools import lru_cache
import hashlib
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import numpy as np
from PIL import Image

# Initialize the FastAPI app
app = FastAPI(
    title="Garbage Classifier API",
    description="Decoupled backend for caching and inference",
)

# Import our ML functions
from app.model import load_model, predict, CLASS_NAMES
from app.utils import preprocess_image, generate_gradcam, overlay_heatmap

# Global variable to store loaded model
model = None


@app.on_event("startup")
def startup_event():
    """Load the model on startup so we don't reload it every request."""
    global model
    try:
        model = load_model()
    except Exception as e:
        print(f"Failed to load model during startup: {e}")


@lru_cache(maxsize=128)
def cached_inference(image_hash: str) -> Dict[str, Any]:
    """
    LRU Cache wrapper for inference. We hash the image bytes before calling this.
    Note: We pass the image_hash just as a cache key, the actual image data is retrieved from a temporary store
    or we could pass the base64 string directly if it's not too huge.
    For simplicity and avoiding large string hashing in memory, we'll hash the image bytes and pass the base64 string.
    """
    pass  # Re-implementing correctly below


# In memory store for cached predictions since lru_cache doesn't work well with large numpy arrays/Pydantic objects directly
_prediction_cache = {}


@app.post("/predict")
async def predict_endpoint(file: UploadFile = File(...)):
    """
    Endpoint for uploading an image and receiving classification predictions.
    Implements inference caching via image hashing.
    """
    global model
    if model is None:
        raise HTTPException(status_code=503, detail="Model is not loaded")

    # Read image bytes
    contents = await file.read()

    # Calculate hash for caching
    image_hash = hashlib.md5(contents).hexdigest()

    # Check cache
    if image_hash in _prediction_cache:
        return JSONResponse(content=_prediction_cache[image_hash])

    try:
        # Load image via PIL
        image = Image.open(io.BytesIO(contents))
        image.load()
        img_rgb = image.convert("RGB")
        img_np = np.array(img_rgb)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image format: {e}")

    try:
        # Run standard inference
        probs = predict(model, image)

        heatmap_base64 = None
        # Run Explainable AI if model is not TFLite
        if not getattr(model, "_is_tflite", False):
            # Determine target size
            try:
                if isinstance(model.input_shape, list):
                    shape = model.input_shape[0]
                else:
                    shape = model.input_shape
                h, w = shape[1], shape[2]
                target_size = (h, w) if h is not None and w is not None else None
            except:
                target_size = None

            processed_img = preprocess_image(image, target_size=target_size)
            input_batch = np.expand_dims(processed_img, axis=0)
            top_idx = int(np.argmax(probs))

            heatmap = generate_gradcam(model, input_batch, top_idx)
            if heatmap is not None:
                heatmap_overlay = overlay_heatmap(heatmap, img_np)

                # Convert back to PIL Image and then base64 for transport
                overlay_pil = Image.fromarray(heatmap_overlay)
                buffered = io.BytesIO()
                overlay_pil.save(buffered, format="JPEG")
                heatmap_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

        # Build response payload
        response_data = {
            "probs": probs,
            "classes": CLASS_NAMES,
            "top_prediction": CLASS_NAMES[int(np.argmax(probs))],
            "heatmap_base64": heatmap_base64,
            "cached": False,
        }

        # Save to cache
        cache_data = response_data.copy()
        cache_data["cached"] = True
        _prediction_cache[image_hash] = cache_data

        return JSONResponse(content=response_data)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference failed: {e}")
