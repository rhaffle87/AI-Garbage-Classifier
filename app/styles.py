"""Styles Module.

Provides custom CSS styling sheets to implement a premium glassmorphic
and dark-accents design theme within Streamlit web app views.
"""

import streamlit as st

def inject_custom_css():
    """Injects custom CSS layout parameters, typography, and bento-cards definitions.

    Imports Google Fonts 'Outfit' and embeds design rules directly into Streamlit's 
    root HTML markup context.
    """
    css = """
    <style>
    /* Import modern typography */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
    
    /* Apply typography and colors */
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Glassmorphism card utility */
    .premium-card {
        background: rgba(255, 255, 255, 0.95);
        border: 1px solid rgba(46, 125, 50, 0.12);
        border-radius: 16px;
        padding: 1.8rem;
        box-shadow: 0 8px 30px rgba(46, 125, 50, 0.04);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        margin-bottom: 1.5rem;
    }
    
    .premium-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 16px 40px rgba(46, 125, 50, 0.1);
        border-color: rgba(46, 125, 50, 0.25);
    }
    
    /* Header Banner styling */
    .header-banner {
        background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 50%, #4CAF50 100%);
        color: white;
        padding: 2.5rem 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(27, 94, 32, 0.15);
        position: relative;
        overflow: hidden;
    }
    
    .header-banner::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: radial-gradient(circle at 80% 20%, rgba(255,255,255,0.15) 0%, transparent 50%);
        pointer-events: none;
    }
    
    .header-banner h1 {
        font-size: 2.8rem !important;
        font-weight: 700 !important;
        color: white !important;
        margin-bottom: 0.5rem !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .header-banner p {
        font-size: 1.15rem !important;
        font-weight: 300 !important;
        color: rgba(255, 255, 255, 0.9) !important;
        max-width: 700px;
        margin: 0 auto !important;
    }

    /* Metric card styles */
    .metric-card {
        background: linear-gradient(145deg, #ffffff, #fcfdfe);
        border: 1px solid rgba(46, 125, 50, 0.1);
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.02);
        border-top: 4px solid #2E7D32;
    }

    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1B5E20;
        margin: 0.2rem 0;
    }

    .metric-label {
        font-size: 0.9rem;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Badges */
    .confidence-badge {
        display: inline-block;
        padding: 0.35em 0.65em;
        font-size: 0.85em;
        font-weight: 600;
        line-height: 1;
        text-align: center;
        white-space: nowrap;
        vertical-align: baseline;
        border-radius: 50rem;
        margin-bottom: 0.5rem;
    }
    
    .badge-high {
        background-color: #E8F5E9;
        color: #2E7D32;
        border: 1px solid #C8E6C9;
    }
    
    .badge-low {
        background-color: #FFF3E0;
        color: #E65100;
        border: 1px solid #FFE0B2;
    }
    
    /* Log console styling */
    .terminal-console {
        background-color: #1E1E1E;
        color: #D4D4D4;
        font-family: 'Courier New', Courier, monospace;
        padding: 1.2rem;
        border-radius: 10px;
        border-left: 6px solid #4CAF50;
        max-height: 350px;
        overflow-y: auto;
        box-shadow: inset 0 0 10px rgba(0,0,0,0.5);
        font-size: 0.85rem;
        line-height: 1.4;
    }
    
    .terminal-line-info { color: #569CD6; }
    .terminal-line-success { color: #4FC1FF; }
    
    /* Category tag chips */
    .category-chip {
        display: inline-flex;
        align-items: center;
        padding: 0.35rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
        background-color: #E8F5E9;
        color: #2E7D32;
        border: 1px solid rgba(46, 125, 50, 0.15);
    }
    
    /* Custom spacing */
    .section-gap {
        margin-top: 2rem;
        margin-bottom: 2rem;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
