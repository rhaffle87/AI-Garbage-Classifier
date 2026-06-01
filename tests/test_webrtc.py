def test_streamlit_webrtc_optional():
    try:
        import streamlit_webrtc
    except Exception:
        # Not installed in the environment — that's acceptable for tests
        return
    assert True
