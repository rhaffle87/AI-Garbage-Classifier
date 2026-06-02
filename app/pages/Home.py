"""Home Dashboard Page.

Implements the application landing page with hero banners, feature grids, 
interactive educational guides, and the dynamic carbon/energy recycling impact 
calculator.
"""

import sys
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import streamlit as st
from app.styles import get_svg_icon, inject_custom_css, get_latest_pipeline_summary

# Apply global premium styling
inject_custom_css()

# Hero Section
st.markdown(f"""
<div class="header-banner">
    <div style="display: flex; justify-content: center; align-items: center; gap: 16px; margin-bottom: 0.8rem;">
        {get_svg_icon("recycle", size=48, color="#FFFFFF")}
        <h1 style="margin: 0 !important; color: white !important;">AI Garbage Classifier</h1>
    </div>
    <p>A smart, modern way to identify and sort your waste using deep learning and neural network image classification.</p>
</div>
""", unsafe_allow_html=True)


# Core Features Grid (using premium cards)
st.markdown(f"""
<div class="flex-header">
    {get_svg_icon("leaf", size=28, color="var(--theme-primary)")}
    <h3 style="color: var(--theme-green-dark); font-weight: 600;">Core Capabilities</h3>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="premium-card">
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 0.5rem;">
            {get_svg_icon("camera", size=22, color="var(--theme-primary)")}
            <h4 style="color: var(--theme-primary); margin: 0;">Instant Predictions</h4>
        </div>
        <p style="font-size: 0.95rem; color: var(--text-color); opacity: 0.85; line-height: 1.5; margin: 0;">
            Upload an image, take a webcam snapshot, or stream live video to instantly classify waste into 6 categories with confidence scores.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="premium-card">
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 0.5rem;">
            {get_svg_icon("cpu", size=22, color="var(--theme-primary)")}
            <h4 style="color: var(--theme-primary); margin: 0;">Transfer Learning</h4>
        </div>
        <p style="font-size: 0.95rem; color: var(--text-color); opacity: 0.85; line-height: 1.5; margin: 0;">
            Leverages a custom MobileNetV2 architecture pretrained on ImageNet. Quick training pipeline customizable for your datasets.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="premium-card">
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 0.5rem;">
            {get_svg_icon("chart", size=22, color="var(--theme-primary)")}
            <h4 style="color: var(--theme-primary); margin: 0;">Deep Evaluation</h4>
        </div>
        <p style="font-size: 0.95rem; color: var(--text-color); opacity: 0.85; line-height: 1.5; margin: 0;">
            Track validation accuracy, classification reports, precision, recall, and visualize results using interactive Confusion Matrices.
        </p>
    </div>
    """, unsafe_allow_html=True)

# MLOps Pipeline Status Section
summary = get_latest_pipeline_summary()
if summary:
    st.divider()
    st.markdown(f"""
    <div class="flex-header">
        {get_svg_icon("cpu", size=28, color="var(--theme-primary)")}
        <h3 style="color: var(--theme-green-dark); font-weight: 600;">Latest MLOps Pipeline Status</h3>
    </div>
    """, unsafe_allow_html=True)
    
    status_color = "color-mix(in srgb, #2E7D32 85%, var(--text-color))" if summary["promoted"] == "Yes" else "color-mix(in srgb, #C62828 85%, var(--text-color))"
    status_bg = "color-mix(in srgb, #2E7D32 12%, var(--background-color))" if summary["promoted"] == "Yes" else "color-mix(in srgb, #C62828 12%, var(--background-color))"
    status_border = "color-mix(in srgb, #2E7D32 25%, transparent)" if summary["promoted"] == "Yes" else "color-mix(in srgb, #C62828 25%, transparent)"
    status_text = "🛡️ PASSED & PROMOTED TO PRODUCTION" if summary["promoted"] == "Yes" else "❌ REJECTED BY QUALITY GATE (Draft Checkpoint)"
    
    col_p1, col_p2 = st.columns([1, 1])
    with col_p1:
        st.markdown(f"""
        <div class="premium-card" style="height: 100%;">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 0.8rem;">
                {get_svg_icon("settings", size=20, color="var(--theme-primary)")}
                <h4 style="color: var(--theme-green-dark); margin: 0; font-size: 1.05rem;">Pipeline Settings & Run Info</h4>
            </div>
            <table style="width: 100%; border-collapse: collapse; font-size: 0.9rem;">
                <tr style="border-bottom: 1px solid color-mix(in srgb, var(--text-color) 10%, transparent); height: 35px;">
                    <td style="color: var(--theme-text-muted); font-weight: 500;">Run Date</td>
                    <td style="text-align: right; font-weight: 600; color: var(--text-color);">{summary["date"]}</td>
                </tr>
                <tr style="border-bottom: 1px solid color-mix(in srgb, var(--text-color) 10%, transparent); height: 35px;">
                    <td style="color: var(--theme-text-muted); font-weight: 500;">Training Duration</td>
                    <td style="text-align: right; font-weight: 600; color: var(--text-color);">{summary["duration"]}</td>
                </tr>
                <tr style="border-bottom: 1px solid color-mix(in srgb, var(--text-color) 10%, transparent); height: 35px;">
                    <td style="color: var(--theme-text-muted); font-weight: 500;">Training Epochs</td>
                    <td style="text-align: right; font-weight: 600; color: var(--text-color);">{summary["epochs"]} epochs</td>
                </tr>
                <tr style="height: 35px;">
                    <td style="color: var(--theme-text-muted); font-weight: 500;">Data Ingestion Format</td>
                    <td style="text-align: right; font-weight: 600; color: var(--text-color);">{summary["format"]}</td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
        
    with col_p2:
        st.markdown(f"""
        <div class="premium-card" style="height: 100%;">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 0.8rem;">
                {get_svg_icon("chart", size=20, color="var(--theme-primary)")}
                <h4 style="color: var(--theme-green-dark); margin: 0; font-size: 1.05rem;">Validation Accuracy & Promotion</h4>
            </div>
            <div style="display: flex; gap: 15px; margin-bottom: 12px;">
                <div style="flex: 1; background-color: color-mix(in srgb, var(--background-color) 96%, var(--text-color) 4%); border: 1px solid color-mix(in srgb, var(--text-color) 8%, transparent); border-radius: 8px; padding: 10px; text-align: center;">
                    <div style="font-size: 0.7rem; color: var(--theme-text-muted); text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px;">Test Accuracy</div>
                    <div style="font-size: 1.5rem; font-weight: 700; color: var(--theme-green-dark); margin-top: 2px;">{summary["accuracy"]}</div>
                </div>
                <div style="flex: 1; background-color: color-mix(in srgb, var(--background-color) 96%, var(--text-color) 4%); border: 1px solid color-mix(in srgb, var(--text-color) 8%, transparent); border-radius: 8px; padding: 10px; text-align: center;">
                    <div style="font-size: 0.7rem; color: var(--theme-text-muted); text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px;">Macro F1-Score</div>
                    <div style="font-size: 1.5rem; font-weight: 700; color: color-mix(in srgb, #0288D1 85%, var(--text-color)); margin-top: 2px;">{summary["f1"]}</div>
                </div>
            </div>
            <div style="background-color: {status_bg}; border: 1px solid {status_border}; border-radius: 8px; padding: 10px; text-align: center;">
                <div style="font-size: 0.65rem; color: var(--theme-text-muted); text-transform: uppercase; font-weight: 700; margin-bottom: 2px; letter-spacing: 0.5px;">Promotion Verdict</div>
                <div style="color: {status_color}; font-weight: 700; font-size: 0.8rem; letter-spacing: 0.2px;">{status_text}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Interactive Section: Recycling Impact Calculator
st.divider()
st.markdown(f"""
<div class="flex-header">
    {get_svg_icon("recycle", size=28, color="var(--theme-primary)")}
    <h3 style="color: var(--theme-green-dark); font-weight: 600;">Recycling Impact Calculator</h3>
</div>
""", unsafe_allow_html=True)
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
        <div style="font-size: 0.85rem; color: var(--theme-text-muted);">CO2 emissions prevented from entering the atmosphere</div>
    </div>
    <div class="metric-card" style="margin-bottom: 1rem;">
        <div class="metric-label">⚡ Energy Conserved</div>
        <div class="metric-value">{energy_saved:.2f} kWh</div>
        <div style="font-size: 0.85rem; color: var(--theme-text-muted);">Equivalent to running a typical LED TV for {energy_saved*30:.1f} hours</div>
    </div>
    <div class="metric-card" style="margin-bottom: 1rem;">
        <div class="metric-label">🗑️ Landfill Space Saved</div>
        <div class="metric-value">{landfill_saved:.1f} Liters</div>
        <div style="font-size: 0.85rem; color: var(--theme-text-muted);">Volume of waste kept out of municipal landfills</div>
    </div>
    """, unsafe_allow_html=True)

# Educational Guide Section
st.divider()
st.markdown(f"""
<div class="flex-header">
    {get_svg_icon("info", size=28, color="var(--theme-primary)")}
    <h3 style="color: var(--theme-green-dark); font-weight: 600;">Waste Sorting Quick Reference</h3>
</div>
""", unsafe_allow_html=True)
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
<div style='text-align: center; margin-top: 3rem; color: var(--theme-text-muted);'>
    <small>Built with ❤️ using Streamlit, TensorFlow & MobileNetV2</small>
</div>
""", unsafe_allow_html=True)
