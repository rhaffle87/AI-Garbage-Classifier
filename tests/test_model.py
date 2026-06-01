from app.model import load_model, predict

def test_load_model():
    model = load_model('models/garbage_model.h5')
    assert model is not None, "Model should be loaded successfully"

def test_predict():
    model = load_model('models/garbage_model.h5')
    # Create a dummy image (128x128 RGB) to simulate a real input
    import numpy as np
    test_image = (np.random.rand(128, 128, 3) * 255).astype('uint8')
    prediction = predict(model, test_image)
    assert prediction is not None, "Prediction should not be None"
    assert isinstance(prediction, list), "Prediction should be a list"
    assert len(prediction) == 6, "Prediction list should have one entry per class (6)"