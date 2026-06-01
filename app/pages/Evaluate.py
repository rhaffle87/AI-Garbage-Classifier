"""Evaluation Page.

Implements model evaluation controls in Streamlit. Users can trigger full 
dataset evaluation sweeps to compute standard precision/recall/f1-score reports,
plot interactive confusion matrices, and review key metrics.
"""

import os
import sys
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from app.model import load_model
from app.config import CLASS_NAMES, DATA_DIR
from app.styles import inject_custom_css

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

st.set_page_config(page_title="Evaluate - Garbage Classifier", page_icon="📊", layout="wide")

# Apply global premium styling
inject_custom_css()

# Header Banner
st.markdown("""
<div class="header-banner" style="background: linear-gradient(135deg, #004d40 0%, #00695c 50%, #00796b 100%);">
    <h1>📊 Evaluate Model Performance</h1>
    <p>Run your trained neural network against the dataset to calculate accuracy metrics and visualize confusion matrices.</p>
</div>
""", unsafe_allow_html=True)

@st.cache_resource
def get_cached_model():
    return load_model()

model = get_cached_model()
if getattr(model, '_is_fallback', False):
    st.warning("⚠️ No valid saved model found — using a small fallback model. To see meaningful evaluation, please train a model first on the **Train** page.")
    st.stop()

# Instructions
st.write("### Model Evaluation Control")
st.markdown("Click the button below to load test images, run predictions, and compile standard classification metrics.")

if st.button("🚀 Run Full Model Evaluation", type="primary", use_container_width=True):
    status = st.status("Evaluating model...", expanded=True)
    with status:
        st.write("Loading validation images and preprocessing...")
        try:
            from scripts.evaluate import evaluate_model
            st.write("Running predictions batch...")
            report, cm = evaluate_model()
            status.update(label="Evaluation Complete!", state="complete", expanded=False)
        except Exception as e:
            status.update(label="Evaluation Failed!", state="error")
            st.error(f"Error during evaluation: {e}")
            st.stop()
            
    st.success("✅ Model metrics successfully compiled!")
    
    st.write("### 📈 Key Metrics Summary")
    
    # Grab metrics
    accuracy = report.get('accuracy', 0)
    macro_avg = report.get('macro avg', {})
    precision = macro_avg.get('precision', 0)
    recall = macro_avg.get('recall', 0)
    f1_score = macro_avg.get('f1-score', 0)
    
    # Metric cards using CSS
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    
    with m_col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Overall Accuracy</div>
            <div class="metric-value">{accuracy*100:.1f}%</div>
            <div style="font-size: 0.8rem; color: #666;">Ratio of correct classifications</div>
        </div>
        """, unsafe_allow_html=True)
        
    with m_col2:
        st.markdown(f"""
        <div class="metric-card" style="border-top-color: #00796b;">
            <div class="metric-label">Macro Precision</div>
            <div class="metric-value">{precision*100:.1f}%</div>
            <div style="font-size: 0.8rem; color: #666;">Ability to avoid false positives</div>
        </div>
        """, unsafe_allow_html=True)
        
    with m_col3:
        st.markdown(f"""
        <div class="metric-card" style="border-top-color: #00796b;">
            <div class="metric-label">Macro Recall</div>
            <div class="metric-value">{recall*100:.1f}%</div>
            <div style="font-size: 0.8rem; color: #666;">Ability to find all positives</div>
        </div>
        """, unsafe_allow_html=True)

    with m_col4:
        st.markdown(f"""
        <div class="metric-card" style="border-top-color: #00796b;">
            <div class="metric-label">Macro F1-Score</div>
            <div class="metric-value">{f1_score*100:.1f}%</div>
            <div style="font-size: 0.8rem; color: #666;">Harmonic mean of precision and recall</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.divider()
    
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.write("#### 📝 Classification Report")
        st.markdown("Precision, recall, and F1-score breakdown per class category:")
        report_df = pd.DataFrame(report).transpose()
        # Drop support column for cleaner display, style format
        if 'support' in report_df.columns:
            report_df['support'] = report_df['support'].astype(int)
        st.dataframe(report_df.style.format({
            "precision": "{:.3%}",
            "recall": "{:.3%}",
            "f1-score": "{:.3%}",
            "support": "{:,}"
        }), use_container_width=True)
        
    with col2:
        st.write("#### 🗺️ Confusion Matrix Heatmap")
        st.markdown("Visual mapping of true target classes vs predicted categories:")
        
        # Plot styled Confusion Matrix
        fig, ax = plt.subplots(figsize=(8, 6))
        # Custom emerald / green-teal hues for the matrix
        sns.heatmap(cm, annot=True, fmt='d', cmap='YlGnBu', 
                    xticklabels=[c.title() for c in CLASS_NAMES], 
                    yticklabels=[c.title() for c in CLASS_NAMES], ax=ax,
                    cbar=True, annot_kws={"size": 12, "weight": "bold"})
        ax.set_ylabel('True Category Label', fontsize=11, fontweight="bold", labelpad=10)
        ax.set_xlabel('Predicted Category Label', fontsize=11, fontweight="bold", labelpad=10)
        
        # Clean figure background
        fig.patch.set_facecolor('none')
        ax.set_facecolor('none')
        plt.tight_layout()
        
        st.pyplot(fig)
