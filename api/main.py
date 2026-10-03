from fastapi import FastAPI, UploadFile, File
import uvicorn
import cv2
import numpy as np
from PIL import Image
import io
from app.model import load_model, predict

app = FastAPI(title="Garbage Classification API")

# Load model globally on startup
model = None
try:
    model = load_model()
except Exception as e:
    print(f"Failed to load model on startup: {e}")


@app.post("/predict")
async def predict_endpoint(file: UploadFile = File(...)):
    if not model:
        return {"error": "Model not loaded properly on server"}

    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        image = np.array(image)
        # Convert RGB to BGR for cv2 processing if needed, though preprocess_image handles it
        if image.shape[-1] == 4:
            image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)

        preds = predict(model, image)
        return {"predictions": preds}
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
