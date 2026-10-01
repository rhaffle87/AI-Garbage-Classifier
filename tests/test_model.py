from app.model import load_model, predict


def test_load_model():
    model = load_model("models/garbage_model.h5")
    assert model is not None, "Model should be loaded successfully"


import pytest


def test_predict():
    model = load_model("models/garbage_model.h5")
    # Create a dummy image (128x128 RGB) to simulate a real input
    import numpy as np

    test_image = (np.random.rand(128, 128, 3) * 255).astype("uint8")
    prediction = predict(model, test_image)
    assert prediction is not None, "Prediction should not be None"
    assert isinstance(prediction, list), "Prediction should be a list"
    assert len(prediction) == 6, "Prediction list should have one entry per class (6)"


def test_predict_invalid_image():
    model = load_model("models/garbage_model.h5")
    import numpy as np

    # Test with empty array (invalid image format)
    test_image = np.array([])
    with pytest.raises(Exception):
        predict(model, test_image)

    # Test with missing file path
    with pytest.raises(ValueError):
        predict(model, "non_existent_image_path.jpg")
