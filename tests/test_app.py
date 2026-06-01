import numpy as np
from app.model import load_model, predict


def test_model_loading():
    model = load_model('models/garbage_model.h5')
    assert model is not None


def test_prediction_with_random_image():
    model = load_model('models/garbage_model.h5')
    img = (np.random.rand(128, 128, 3) * 255).astype('uint8')
    preds = predict(model, img)
    assert isinstance(preds, list)
    assert len(preds) == 6