"""Predict Page.

Provides interfaces for uploading raw garbage images or capturing them via webcam,
preprocesses them, runs inference against the loaded neural network model,
displays probability metrics, and presents recycling instructions.
"""

import streamlit as st
import cv2
import numpy as np
from PIL import Image
from app.model import load_model, predict
from app.config import CLASS_NAMES
from app.styles import inject_custom_css

st.set_page_config(page_title="Predict - Garbage Classifier", page_icon="🔮", layout="wide")

# Inject premium visual elements
inject_custom_css()

@st.cache_resource
def get_cached_model():
    return load_model()

model = get_cached_model()
if getattr(model, '_is_fallback', False):
    st.warning("⚠️ No valid saved model found — using a small fallback model. For meaningful results, train and save a model first on the Train page.")

# Page Header
st.markdown("""
<div class="header-banner" style="background: linear-gradient(135deg, #0d47a1 0%, #1565c0 50%, #1976d2 100%); box-shadow: 0 10px 30px rgba(13, 71, 161, 0.15);">
    <h1>🔮 Classify Garbage</h1>
    <p>Upload a photo or capture a snapshot to instantly identify waste and learn how to recycle it properly.</p>
</div>
""", unsafe_allow_html=True)

# Recycling tips dictionary
RECYCLING_TIPS = {
    'cardboard': "📦 **Cardboard**: Remove packaging tape, flatten the box completely to save space, and make sure it remains clean and dry. Wet or greasy cardboard cannot be recycled and should go in the compost or trash.",
    'glass': "🍶 **Glass**: Rinse thoroughly to remove food or drink residue. Labels and adhesive can usually stay, but metal/plastic lids should be removed and recycled separately.",
    'metal': "🥫 **Metal**: Rinse aluminum/tin cans to prevent pests. You can crush cans to save space. Clean foil can also be recycled; squeeze it into a tight ball before throwing it in the bin.",
    'paper': "📝 **Paper**: Keep paper dry. Office paper, newspapers, letters, and books are highly recyclable. Avoid recycling soiled paper, paper towels, tissues, or paper contaminated with food.",
    'plastic': "🥤 **Plastic**: Empty and rinse containers. Squeeze the bottle to remove air and replace the cap. Check local guidelines to see which plastic numbers (e.g., #1 PETE, #2 HDPE) are accepted.",
    'trash': "🗑️ **Trash**: This item cannot be recycled with the current sorted streams. Please place it in the general waste bin. Consider composting if it is organic waste."
}

def display_predictions(probs, image_obj):
    col1, col2 = st.columns([1.1, 1])
    
    with col1:
        st.write("#### 📸 Analyzed Visual")
        if isinstance(image_obj, Image.Image):
            st.image(image_obj, use_column_width=True)
        else:
            st.image(image_obj, channels="RGB", use_column_width=True)
            
    with col2:
        st.write("#### 📊 Classification Output")
        top_indices = np.argsort(probs)[::-1]
        top_class = CLASS_NAMES[top_indices[0]]
        max_prob = probs[top_indices[0]]
        
        # Render a premium styled card for results
        confidence_text = f"Confidence: {max_prob*100:.1f}%"
        if max_prob < 0.50:
            badge_html = f'<span class="confidence-badge badge-low">⚠️ Low Confidence ({max_prob*100:.1f}%)</span>'
            status_alert = st.warning(f"The model is slightly unsure, but it's likely **{top_class.title()}**.")
        else:
            badge_html = f'<span class="confidence-badge badge-high">✅ High Confidence ({max_prob*100:.1f}%)</span>'
            status_alert = st.success(f"Successfully identified as **{top_class.title()}**!")

        st.markdown(f"""
        <div class="premium-card">
            {badge_html}
            <h3 style="margin: 0.5rem 0 1rem 0; color: #1B5E20;">{top_class.title()}</h3>
            <p style="font-size: 0.95rem; line-height: 1.5; color: #555; margin-bottom: 0;">
                {RECYCLING_TIPS.get(top_class, "Follow general recycling instructions.")}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("**Top Predictions Probability Distribution:**")
        for i, idx in enumerate(top_indices[:3]):
            class_name = CLASS_NAMES[idx].title()
            prob = float(probs[idx])
            
            col_lbl, col_bar = st.columns([1, 2])
            with col_lbl:
                st.write(f"**{class_name}** ({prob*100:.1f}%)")
            with col_bar:
                st.progress(prob)

st.write("### Choose Input Source")
tab1, tab2, tab3 = st.tabs(["📁 Upload Image File", "📸 Webcam Snapshot", "🎥 Live Camera Stream"])

with tab1:
    st.markdown("""
    <div style="padding: 1rem 0;">
        <p style="color: #666; font-size: 0.95rem;">Upload a JPEG or PNG photograph from your local storage.</p>
    </div>
    """, unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Choose an image file...", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
    if uploaded_file is not None:
        with st.spinner("Processing image via neural network..."):
            image = Image.open(uploaded_file)
            probs = predict(model, image)
            st.divider()
            display_predictions(probs, image)

with tab2:
    st.markdown("""
    <div style="padding: 1rem 0;">
        <p style="color: #666; font-size: 0.95rem;">Capture a single photo using your integrated laptop camera or webcam.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("📸 Capture Webcam Photo", use_container_width=True, type="primary"):
        with st.spinner("Activating camera..."):
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                st.error("❌ Could not access the webcam. Check camera permissions in your OS/browser.")
            else:
                ret, frame = cap.read()
                cap.release()
                if not ret:
                    st.error("❌ Failed to capture image from camera stream.")
                else:
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    probs = predict(model, frame_rgb)
                    st.divider()
                    display_predictions(probs, frame_rgb)

with tab3:
    st.markdown("""
    <div style="padding: 1rem 0;">
        <p style="color: #666; font-size: 0.95rem;">Enable real-time continuous classification directly inside your browser window.</p>
    </div>
    """, unsafe_allow_html=True)
    try:
        from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
        
        class GarbageTransformer(VideoTransformerBase):
            def __init__(self):
                super().__init__()
                self.model = model
                self.class_names = CLASS_NAMES

            def recv(self, frame):
                import av
                import cv2
                from app.model import predict

                img = frame.to_ndarray(format="bgr24")
                rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                try:
                    preds = predict(self.model, rgb)
                    top_idx = int(np.argmax(preds))
                    
                    if preds[top_idx] < 0.5:
                        label = f"Unsure ({preds[top_idx]*100:.1f}%)"
                        color = (0, 165, 255) # Orange in BGR
                    else:
                        label = f"{self.class_names[top_idx].title()}: {preds[top_idx]*100:.1f}%"
                        color = (0, 255, 0) # Green in BGR
                except Exception:
                    label = "Processing..."
                    color = (255, 255, 255)

                cv2.putText(img, label, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)
                return av.VideoFrame.from_ndarray(img, format="bgr24")

        webrtc_streamer(key="garbage-webrtc", video_transformer_factory=GarbageTransformer,
                        media_stream_constraints={"video": True, "audio": False})
    except Exception:
        st.error("`streamlit-webrtc` is not fully configured or installed. Please verify installation packages.")