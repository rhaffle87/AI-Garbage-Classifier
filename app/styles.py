"""Styles Module.

Provides custom CSS styling sheets to implement a premium glassmorphic
and dark-accents design theme within Streamlit web app views.
"""

import streamlit as st

def get_svg_icon(icon_name, size=24, color="currentColor"):
    """Returns raw HTML for Lucide SVG icons to avoid using low-quality emojis as icons."""
    icons = {
        "camera": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3z"/><circle cx="12" cy="13" r="3"/></svg>',
        "cpu": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="16" height="16" x="4" y="4" rx="2"/><rect width="6" height="6" x="9" y="9" rx="1"/><path d="M9 1v3"/><path d="M15 1v3"/><path d="M9 20v3"/><path d="M15 20v3"/><path d="M20 9h3"/><path d="M20 15h3"/><path d="M1 9h3"/><path d="M1 15h3"/></svg>',
        "chart": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3v18h18"/><path d="m19 9-5 5-4-4-3 3"/></svg>',
        "home": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>',
        "refresh": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a9 9 0 0 0-9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/><path d="M3 12a9 9 0 0 0 9 9 9.75 9.75 0 0 0 6.74-2.74L21 16"/><path d="M16 16h5v5"/></svg>',
        "stop": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="7.86 2 16.14 2 22 7.86 22 16.14 16.14 22 7.86 22 2 16.14 2 7.86 7.86 2"/><line x1="9" x2="15" y1="9" y2="15"/><line x1="15" x2="9" y1="9" y2="15"/></svg>',
        "info": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>',
        "terminal": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="4 17 10 11 4 5"/><line x1="12" x2="20" y1="19" y2="19"/></svg>',
        "check": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg>',
        "alert": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" x2="12" y1="9" y2="13"/><line x1="12" x2="12" y1="17" y2="17"/></svg>',
        "settings": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>',
        "shield": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
        "search": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>',
        "trash": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/><line x1="10" x2="10" y1="11" y2="17"/><line x1="14" x2="14" y1="11" y2="17"/></svg>',
        "play": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="6 3 20 12 6 21 6 3"/></svg>',
        "recycle": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 11h13V4"/><path d="m16 7 4 4-4 4"/><path d="M17 13v7H4v-7"/><path d="m8 17-4-4 4-4"/><path d="M12 2v5h5"/><path d="m13 6 4 4-4 4"/></svg>',
        "leaf": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 3.5 1 8a7 7 0 0 1-9 10Z"/><path d="M9 22v-4h4"/></svg>'
    }
    return icons.get(icon_name, "")

def inject_custom_css():
    """Injects custom CSS layout parameters, typography, and bento-cards definitions.

    Imports Google Fonts 'Outfit' and embeds design rules directly into Streamlit's 
    root HTML markup context, fully supporting Light, Dark, and Custom themes dynamically.
    """
    css = """
    <style>
    /* Import modern typography */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap&font-display=swap');
    
    /* Theme variable mapping based on active Streamlit theme */
    :root {
        --theme-primary: var(--primary-color);
        --theme-green-dark: color-mix(in srgb, var(--primary-color) 85%, var(--text-color));
        --theme-green-light: color-mix(in srgb, var(--primary-color) 70%, #ffffff 30%);
        
        /* Dynamic card tokens */
        --theme-card-bg: color-mix(in srgb, var(--background-color) 94%, var(--text-color) 6%);
        --theme-card-border: color-mix(in srgb, var(--primary-color) 15%, transparent);
        --theme-card-shadow: 0 8px 30px color-mix(in srgb, var(--text-color) 4%, transparent);
        --theme-card-shadow-hover: 0 16px 40px color-mix(in srgb, var(--primary-color) 12%, transparent);
        
        /* Text muted */
        --theme-text-muted: color-mix(in srgb, var(--text-color) 60%, transparent);
        
        /* Banners */
        --theme-banner-bg: linear-gradient(135deg, 
            color-mix(in srgb, var(--primary-color) 80%, #000) 0%, 
            var(--primary-color) 50%, 
            color-mix(in srgb, var(--primary-color) 80%, #fff) 100%
        );
    }
    
    /* Apply typography and colors with system fallbacks to prevent font shift flashing */
    html, body, [class*="css"] {
        font-family: 'Outfit', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
    }
    
    /* Header layout alignment helper */
    .flex-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    .flex-header h1, .flex-header h2, .flex-header h3 {
        margin: 0 !important;
    }
    
    /* Glassmorphism card utility */
    .premium-card {
        background: var(--theme-card-bg) !important;
        color: var(--text-color) !important;
        border: 1px solid var(--theme-card-border) !important;
        border-radius: 16px;
        padding: 1.8rem;
        box-shadow: var(--theme-card-shadow) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        margin-bottom: 1.5rem;
        cursor: pointer;
    }
    
    .premium-card:hover {
        transform: translateY(-4px) !important;
        box-shadow: var(--theme-card-shadow-hover) !important;
        border-color: var(--theme-primary) !important;
    }
    
    /* Header Banner styling */
    .header-banner {
        background: var(--theme-banner-bg) !important;
        color: white !important;
        padding: 2.5rem 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px color-mix(in srgb, var(--primary-color) 20%, transparent) !important;
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
        background: var(--theme-card-bg) !important;
        border: 1px solid var(--theme-card-border) !important;
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        box-shadow: var(--theme-card-shadow) !important;
        border-top: 4px solid var(--theme-primary) !important;
    }
 
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: var(--theme-green-dark) !important;
        margin: 0.2rem 0;
    }
 
    .metric-label {
        font-size: 0.9rem;
        color: var(--theme-text-muted) !important;
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
        background-color: color-mix(in srgb, #2E7D32 12%, var(--background-color)) !important;
        color: color-mix(in srgb, #2E7D32 85%, var(--text-color)) !important;
        border: 1px solid color-mix(in srgb, #2E7D32 25%, transparent) !important;
    }
    
    .badge-low {
        background-color: color-mix(in srgb, #E65100 12%, var(--background-color)) !important;
        color: color-mix(in srgb, #E65100 85%, var(--text-color)) !important;
        border: 1px solid color-mix(in srgb, #E65100 25%, transparent) !important;
    }
    
    /* Log console styling */
    .terminal-console {
        background-color: #1E1E1E !important;
        color: #D4D4D4 !important;
        font-family: 'Courier New', Courier, monospace;
        padding: 1.2rem;
        border-radius: 10px;
        border-left: 6px solid var(--theme-primary) !important;
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
        background-color: color-mix(in srgb, var(--primary-color) 12%, var(--background-color)) !important;
        color: color-mix(in srgb, var(--primary-color) 85%, var(--text-color)) !important;
        border: 1px solid color-mix(in srgb, var(--primary-color) 20%, transparent) !important;
    }
    
    /* Custom spacing */
    .section-gap {
        margin-top: 2rem;
        margin-bottom: 2rem;
    }
    
    /* Premium Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: var(--secondary-background-color) !important;
        border-right: 1px solid color-mix(in srgb, var(--primary-color) 8%, transparent) !important;
    }
    
    [data-testid="stSidebarNav"] {
        padding-top: 2rem !important;
    }
    
    /* Branding title at the top of the sidebar list */
    [data-testid="stSidebarNav"]::before {
        content: "Garbage Classifier" !important;
        display: block !important;
        padding: 0px 24px 1.5rem 24px !important;
        font-family: 'Outfit', sans-serif !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        color: var(--theme-green-dark) !important;
        letter-spacing: -0.3px !important;
        border-bottom: 1px solid color-mix(in srgb, var(--primary-color) 8%, transparent) !important;
        margin-bottom: 1rem !important;
    }
    
    [data-testid="stSidebarNav"] ul {
        padding: 0 !important;
        list-style: none !important;
    }
    
    [data-testid="stSidebarNav"] ul li {
        padding: 0 !important;
        margin: 4px 14px !important;
    }
    
    [data-testid="stSidebarNav"] ul li a {
        display: flex !important;
        align-items: center !important;
        padding: 10px 16px !important;
        border-radius: 12px !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 500 !important;
        color: var(--text-color) !important;
        background-color: transparent !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        text-decoration: none !important;
        opacity: 0.8;
    }
    
    /* Hide default streamlit page icon span ONLY if it's the icon (first of multiple spans) */
    [data-testid="stSidebarNav"] ul li a span:first-child:not(:last-child) {
        display: none !important;
    }
    
    /* Base pseudo-element styling for icons */
    [data-testid="stSidebarNav"] ul li a::before {
        content: "" !important;
        display: inline-block !important;
        width: 18px !important;
        height: 18px !important;
        margin-right: 12px !important;
        background-repeat: no-repeat !important;
        background-size: contain !important;
        background-position: center !important;
        transition: all 0.2s ease !important;
    }
    
    /* Hover state */
    [data-testid="stSidebarNav"] ul li a:hover {
        background-color: color-mix(in srgb, var(--primary-color) 8%, transparent) !important;
        color: var(--theme-green-dark) !important;
        opacity: 1 !important;
    }
    
    /* Active navigation link */
    [data-testid="stSidebarNav"] ul li a[aria-current="page"] {
        background-color: color-mix(in srgb, var(--primary-color) 12%, transparent) !important;
        color: var(--theme-primary) !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 12px color-mix(in srgb, var(--primary-color) 6%, transparent) !important;
        opacity: 1 !important;
    }

    /* Rename first link 'streamlit app' to 'Home' */
    [data-testid="stSidebarNav"] ul li:first-child a span {
        font-size: 0 !important;
    }
    
    [data-testid="stSidebarNav"] ul li:first-child a span::after {
        content: "Home" !important;
        font-size: 14px !important;
        font-weight: inherit !important;
        color: inherit !important;
    }
    
    /* URL encoded SVGs for sidebar link icons */
    /* 1. Home Link Icon */
    [data-testid="stSidebarNav"] ul li:nth-child(1) a::before {
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='18' height='18' viewBox='0 0 24 24' fill='none' stroke='%234b5563' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z'/%3E%3Cpolyline points='9 22 9 12 15 12 15 22'/%3E%3C/svg%3E") !important;
    }
    [data-testid="stSidebarNav"] ul li:nth-child(1) a[aria-current="page"]::before,
    [data-testid="stSidebarNav"] ul li:nth-child(1) a:hover::before {
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='18' height='18' viewBox='0 0 24 24' fill='none' stroke='%232e7d32' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z'/%3E%3Cpolyline points='9 22 9 12 15 12 15 22'/%3E%3C/svg%3E") !important;
    }
    
    /* 2. Evaluate Link Icon */
    [data-testid="stSidebarNav"] ul li:nth-child(2) a::before {
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='18' height='18' viewBox='0 0 24 24' fill='none' stroke='%234b5563' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M3 3v18h18'/%3E%3Cpath d='m19 9-5 5-4-4-3 3'/%3E%3C/svg%3E") !important;
    }
    [data-testid="stSidebarNav"] ul li:nth-child(2) a[aria-current="page"]::before,
    [data-testid="stSidebarNav"] ul li:nth-child(2) a:hover::before {
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='18' height='18' viewBox='0 0 24 24' fill='none' stroke='%232e7d32' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M3 3v18h18'/%3E%3Cpath d='m19 9-5 5-4-4-3 3'/%3E%3C/svg%3E") !important;
    }
    
    /* 3. Predict Link Icon */
    [data-testid="stSidebarNav"] ul li:nth-child(3) a::before {
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='18' height='18' viewBox='0 0 24 24' fill='none' stroke='%234b5563' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3z'/%3E%3Ccircle cx='12' cy='13' r='3'/%3E%3C/svg%3E") !important;
    }
    [data-testid="stSidebarNav"] ul li:nth-child(3) a[aria-current="page"]::before,
    [data-testid="stSidebarNav"] ul li:nth-child(3) a:hover::before {
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='18' height='18' viewBox='0 0 24 24' fill='none' stroke='%232e7d32' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3z'/%3E%3Ccircle cx='12' cy='13' r='3'/%3E%3C/svg%3E") !important;
    }
    
    /* 4. Train Link Icon */
    [data-testid="stSidebarNav"] ul li:nth-child(4) a::before {
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='18' height='18' viewBox='0 0 24 24' fill='none' stroke='%234b5563' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Crect width='16' height='16' x='4' y='4' rx='2'/%3E%3Crect width='6' height='6' x='9' y='9' rx='1'/%3E%3Cpath d='M9 1v3'/%3E%3Cpath d='M15 1v3'/%3E%3Cpath d='M9 20v3'/%3E%3Cpath d='M15 20v3'/%3E%3Cpath d='M20 9h3'/%3E%3Cpath d='M20 15h3'/%3E%3Cpath d='M1 9h3'/%3E%3Cpath d='M1 15h3'/%3E%3C/svg%3E") !important;
    }
    [data-testid="stSidebarNav"] ul li:nth-child(4) a[aria-current="page"]::before,
    [data-testid="stSidebarNav"] ul li:nth-child(4) a:hover::before {
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='18' height='18' viewBox='0 0 24 24' fill='none' stroke='%232e7d32' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Crect width='16' height='16' x='4' y='4' rx='2'/%3E%3Crect width='6' height='6' x='9' y='9' rx='1'/%3E%3Cpath d='M9 1v3'/%3E%3Cpath d='M15 1v3'/%3E%3Cpath d='M9 20v3'/%3E%3Cpath d='M15 20v3'/%3E%3Cpath d='M20 9h3'/%3E%3Cpath d='M20 15h3'/%3E%3Cpath d='M1 9h3'/%3E%3Cpath d='M1 15h3'/%3E%3C/svg%3E") !important;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def render_sidebar_model_status():
    """Renders active model validation & promotion status inside the Streamlit sidebar."""
    import os
    from datetime import datetime
    from app.config import PROD_MODEL_PATH, MODEL_PATH, LEGACY_MODEL_PATH
    
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"""
    <div style="padding: 10px 0 5px 0;">
        <h4 style="margin: 0; color: var(--theme-green-dark); display: flex; align-items: center; gap: 8px; font-size: 1.05rem; font-weight: 600;">
            {get_svg_icon("shield", size=18, color="var(--theme-primary)")}
            <span>Model Status</span>
        </h4>
    </div>
    """, unsafe_allow_html=True)
    
    if os.path.exists(PROD_MODEL_PATH):
        mtime = os.path.getmtime(PROD_MODEL_PATH)
        dt = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M')
        st.sidebar.markdown(f"""
        <div style="background-color: color-mix(in srgb, #2E7D32 12%, var(--background-color)); border: 1px solid color-mix(in srgb, #2E7D32 25%, transparent); border-radius: 12px; padding: 12px; margin-bottom: 10px; box-shadow: var(--theme-card-shadow);">
            <div style="color: color-mix(in srgb, #2E7D32 85%, var(--text-color)); font-weight: 700; font-size: 0.8rem; letter-spacing: 0.5px;">🛡️ PRODUCTION PROMOTED</div>
            <div style="color: var(--text-color); opacity: 0.85; font-size: 0.75rem; margin-top: 4px; line-height: 1.4;">Active model met the 75% accuracy quality gate constraint.</div>
            <div style="color: var(--text-color); opacity: 0.5; font-size: 0.7rem; margin-top: 8px; font-weight: 500;">Last Promoted: {dt}</div>
        </div>
        """, unsafe_allow_html=True)
    elif os.path.exists(MODEL_PATH):
        mtime = os.path.getmtime(MODEL_PATH)
        dt = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M')
        st.sidebar.markdown(f"""
        <div style="background-color: color-mix(in srgb, #E65100 12%, var(--background-color)); border: 1px solid color-mix(in srgb, #E65100 25%, transparent); border-radius: 12px; padding: 12px; margin-bottom: 10px; box-shadow: var(--theme-card-shadow);">
            <div style="color: color-mix(in srgb, #E65100 85%, var(--text-color)); font-weight: 700; font-size: 0.8rem; letter-spacing: 0.5px;">⚠️ CHECKPOINT DRAFT</div>
            <div style="color: var(--text-color); opacity: 0.85; font-size: 0.75rem; margin-top: 4px; line-height: 1.4;">Latest training checkpoint. Quality gate not yet passed/evaluated.</div>
            <div style="color: var(--text-color); opacity: 0.5; font-size: 0.7rem; margin-top: 8px; font-weight: 500;">Saved: {dt}</div>
        </div>
        """, unsafe_allow_html=True)
    elif os.path.exists(LEGACY_MODEL_PATH):
        mtime = os.path.getmtime(LEGACY_MODEL_PATH)
        dt = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M')
        st.sidebar.markdown(f"""
        <div style="background-color: color-mix(in srgb, var(--text-color) 8%, var(--background-color)); border: 1px solid color-mix(in srgb, var(--text-color) 15%, transparent); border-radius: 12px; padding: 12px; margin-bottom: 10px; box-shadow: var(--theme-card-shadow);">
            <div style="color: color-mix(in srgb, var(--text-color) 75%, transparent); font-weight: 700; font-size: 0.8rem; letter-spacing: 0.5px;">📁 LEGACY FALLBACK</div>
            <div style="color: var(--text-color); opacity: 0.85; font-size: 0.75rem; margin-top: 4px; line-height: 1.4;">Using legacy model binary.</div>
            <div style="color: var(--text-color); opacity: 0.5; font-size: 0.7rem; margin-top: 8px; font-weight: 500;">Saved: {dt}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.sidebar.markdown("""
        <div style="background-color: color-mix(in srgb, #C62828 12%, var(--background-color)); border: 1px solid color-mix(in srgb, #C62828 25%, transparent); border-radius: 12px; padding: 12px; margin-bottom: 10px;">
            <div style="color: color-mix(in srgb, #C62828 85%, var(--text-color)); font-weight: 700; font-size: 0.8rem; letter-spacing: 0.5px;">❌ NO TRAINED MODEL</div>
            <div style="color: var(--text-color); opacity: 0.85; font-size: 0.75rem; margin-top: 4px; line-height: 1.4;">Active inference is falling back to untrained dummy classifier.</div>
        </div>
        """, unsafe_allow_html=True)

def get_latest_pipeline_summary():
    """Parses and returns the latest MLOps pipeline summary log as a dictionary."""
    import os
    import re
    from app.config import LOGS_DIR
    
    summary_path = os.path.join(LOGS_DIR, 'pipeline_run_summary.md')
    if not os.path.exists(summary_path):
        return None
        
    try:
        with open(summary_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        date_match = re.search(r"Generated on: (.*)", content)
        duration_match = re.search(r"Duration: (.*) seconds", content)
        epochs_match = re.search(r"- Epochs: (.*)", content)
        format_match = re.search(r"- Streaming Format: (.*)", content)
        accuracy_match = re.search(r"- \*\*Test Accuracy\*\*: (.*)%", content)
        f1_match = re.search(r"- \*\*Macro F1-Score\*\*: (.*)%", content)
        promoted_match = re.search(r"- \*\*Promoted to Production\*\*: (.*)", content)
        
        return {
            "date": date_match.group(1).strip() if date_match else "N/A",
            "duration": duration_match.group(1).strip() if duration_match else "N/A",
            "epochs": epochs_match.group(1).strip() if epochs_match else "N/A",
            "format": format_match.group(1).strip() if format_match else "N/A",
            "accuracy": accuracy_match.group(1).strip() if accuracy_match else "N/A",
            "f1": f1_match.group(1).strip() if f1_match else "N/A",
            "promoted": "Yes" if (promoted_match and "YES" in promoted_match.group(1)) else "No"
        }
    except Exception:
        return None

