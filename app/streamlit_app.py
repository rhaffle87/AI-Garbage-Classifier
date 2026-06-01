"""Main Entry Point and Dashboard.

Implements the application landing page with hero banners, feature grids, 
interactive educational guides, and the dynamic carbon/energy recycling impact 
calculator.
"""

import sys
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import streamlit as st
from app.styles import inject_custom_css

st.set_page_config(
    page_title="AI Garbage Classifier", 
    page_icon="♻️",
    layout="wide"
)

# Apply global premium styling
inject_custom_css()

# Hero Section
st.markdown("""
<div class="header-banner">
    <h1>AI Garbage Classifier ♻️</h1>
    <p>A smart, modern way to identify and sort your waste using deep learning and neural network image classification.</p>
</div>
""", unsafe_allow_html=True)

# Core Features Grid (using premium cards)
st.write("### 🚀 Core Capabilities")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="premium-card">
        <h4 style="color: #2E7D32; margin-top: 0;">🔮 Instant Predictions</h4>
        <p style="font-size: 0.95rem; color: #555; line-height: 1.5;">
            Upload an image, take a webcam snapshot, or stream live video to instantly classify waste into 6 categories with confidence scores.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="premium-card">
        <h4 style="color: #2E7D32; margin-top: 0;">🧠 Transfer Learning</h4>
        <p style="font-size: 0.95rem; color: #555; line-height: 1.5;">
            Leverages a custom MobileNetV2 architecture pretrained on ImageNet. Quick training pipeline customizable for your datasets.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="premium-card">
        <h4 style="color: #2E7D32; margin-top: 0;">📊 Deep Evaluation</h4>
        <p style="font-size: 0.95rem; color: #555; line-height: 1.5;">
            Track validation accuracy, classification reports, precision, recall, and visualize results using interactive Confusion Matrices.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Interactive Section: Recycling Impact Calculator
st.divider()
st.write("### 🌱 Recycling Impact Calculator")
st.markdown("Select or enter the items you are planning to recycle to see the estimated positive impact on our planet!")

calc_col1, calc_col2 = st.columns([1, 1])

with calc_col1:
    st.markdown("#### Input Recyclables")
    cardboard_qty = st.number_input("Cardboard boxes", min_value=0, max_value=1000, value=2, step=1)
    glass_qty = st.number_input("Glass bottles/jars", min_value=0, max_value=1000, value=5, step=1)
    metal_qty = st.number_input("Metal/Aluminum cans", min_value=0, max_value=1000, value=8, step=1)
    paper_qty = st.number_input("Paper sheets", min_value=0, max_value=5000, value=25, step=5)
    plastic_qty = st.number_input("Plastic bottles/containers", min_value=0, max_value=1000, value=12, step=1)

with calc_col2:
    st.markdown("#### Environmental Savings Output")
    
    # Calculation formulas based on EPA standard averages
    co2_saved = (cardboard_qty * 0.22) + (glass_qty * 0.12) + (metal_qty * 0.18) + (paper_qty * 0.015) + (plastic_qty * 0.08)
    energy_saved = (cardboard_qty * 0.5) + (glass_qty * 0.3) + (metal_qty * 0.8) + (paper_qty * 0.05) + (plastic_qty * 0.4)
    landfill_saved = (cardboard_qty * 3.5) + (glass_qty * 0.8) + (metal_qty * 0.4) + (paper_qty * 0.05) + (plastic_qty * 1.5)
    
    # Display savings as custom cards
    st.markdown(f"""
    <div class="metric-card" style="margin-bottom: 1rem;">
        <div class="metric-label">💨 Carbon Footprint Reduced</div>
        <div class="metric-value">{co2_saved:.2f} kg</div>
        <div style="font-size: 0.85rem; color: #666;">CO2 emissions prevented from entering the atmosphere</div>
    </div>
    <div class="metric-card" style="margin-bottom: 1rem;">
        <div class="metric-label">⚡ Energy Conserved</div>
        <div class="metric-value">{energy_saved:.2f} kWh</div>
        <div style="font-size: 0.85rem; color: #666;">Equivalent to running a typical LED TV for {energy_saved*30:.1f} hours</div>
    </div>
    <div class="metric-card" style="margin-bottom: 1rem;">
        <div class="metric-label">🗑️ Landfill Space Saved</div>
        <div class="metric-value">{landfill_saved:.1f} Liters</div>
        <div style="font-size: 0.85rem; color: #666;">Volume of waste kept out of municipal landfills</div>
    </div>
    """, unsafe_allow_html=True)

# Educational Guide Section
st.divider()
st.write("### ♻️ Waste Sorting Quick Reference")
with st.expander("Learn about the 6 waste categories classified by this AI"):
    st.markdown("""
    - **📦 Cardboard**: Boxes, packaging materials, shipping boxes, thick paperboard. *Tip: Keep dry and flatten.*
    - **🍶 Glass**: Beverage bottles, jars, glass containers. *Tip: Rinse out remaining liquids/food particles.*
    - **🥫 Metal**: Soda cans, soup cans, tin/aluminum foil, metal jar lids. *Tip: Crushing cans saves sorting space.*
    - **📝 Paper**: Newspapers, letters, office paper, notebooks, junk mail. *Tip: Ensure there is no wax coating.*
    - **🥤 Plastic**: Water bottles, food containers, detergent jugs, plastic cups. *Tip: Check local resin codes.*
    - **🗑️ Trash**: General non-recyclable waste, soiled items, wrappers, organic residue. *Tip: Place in black bin.*
    """)

st.divider()
st.info("👈 **Use the sidebar** to navigate between pages. Start by checking out the **Predict** page to see it in action!")

st.markdown("""
<div style='text-align: center; margin-top: 3rem; color: #888;'>
    <small>Built with ❤️ using Streamlit, TensorFlow & MobileNetV2</small>
</div>
""", unsafe_allow_html=True)