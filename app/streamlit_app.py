"""Main Entry Point and Routing Controller.

Sets up page configurations, applies global CSS overrides, and manages routing
between dashboard pages using modern Streamlit navigation to prevent FOUC (flash
of unstyled content).
"""

import sys
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import streamlit as st
from app.styles import inject_custom_css

# Apply page config globally before rendering any elements
st.set_page_config(
    page_title="AI Garbage Classifier", 
    page_icon="♻️",
    layout="wide"
)

# Apply global premium styling
inject_custom_css()

# Define multi-page application structure using standard Streamlit Pages
home_page = st.Page("pages/Home.py", title="Home", icon=":material/home:", default=True)
evaluate_page = st.Page("pages/Evaluate.py", title="Evaluate", icon=":material/analytics:")
predict_page = st.Page("pages/Predict.py", title="Predict", icon=":material/photo_camera:")
train_page = st.Page("pages/Train.py", title="Train", icon=":material/settings:")

# Run the navigation controller
pg = st.navigation([home_page, evaluate_page, predict_page, train_page])
pg.run()