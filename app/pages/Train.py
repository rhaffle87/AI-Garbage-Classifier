"""Training Configuration Page.

Enables interactive settings for deep learning training parameters (epochs, batch size),
displays class training distribution charts, triggers asynchronous background training runs,
and renders real-time terminal progress console updates.
"""

import streamlit as st
import os
import sys
import subprocess
import pandas as pd
from app.config import DATA_DIR, CLASS_NAMES
from app.utils import download_dataset_if_missing
from app.styles import inject_custom_css, get_svg_icon

# Apply premium visual design elements
inject_custom_css()

@st.cache_data
def get_dataset_counts():
    counts = {}
    for c in CLASS_NAMES:
        c_dir = os.path.join(DATA_DIR, c)
        if os.path.exists(c_dir):
            counts[c] = len([f for f in os.listdir(c_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
        else:
            counts[c] = 0
    return counts

def main():
    st.markdown(f"""
    <div class="header-banner">
        <div style="display: flex; justify-content: center; align-items: center; gap: 16px; margin-bottom: 0.8rem;">
            {get_svg_icon("settings", size=48, color="#FFFFFF")}
            <h1 style="margin: 0 !important; color: white !important;">Train AI Model</h1>
        </div>
        <p>Configure training hyperparameters, review your local training dataset distribution, and train your custom Deep Learning classifier.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Dataset summary section
    st.markdown(f"""
    <div class="flex-header">
        {get_svg_icon("chart", size=28, color="var(--theme-primary)")}
        <h3 style="color: var(--theme-green-dark); font-weight: 600;">Dataset Distribution</h3>
    </div>
    """, unsafe_allow_html=True)
    counts = get_dataset_counts()
    total_images = sum(counts.values())
    
    col_metric, col_chart = st.columns([1, 2.5])
    
    with col_metric:
        st.markdown(f"""
        <div class="metric-card" style="margin-top: 1rem;">
            <div class="metric-label">Total Images Loaded</div>
            <div class="metric-value">{total_images:,}</div>
            <div style="font-size: 0.85rem; color: var(--theme-text-muted); margin-top: 0.5rem;">
                Images split across 6 classes of waste materials.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Verify / Download dataset button
        st.write("")
        if st.button("🔄 Sync / Verify Dataset", use_container_width=True):
            status = st.status("Verifying active dataset...")
            with status:
                st.write("Checking archive & Kaggle for dataset files...")
                download_dataset_if_missing()
                status.update(label="Dataset Synchronized!", state="complete", expanded=False)
            st.success("✅ Dataset verification finished. Ready to train.")
            st.rerun()

    with col_chart:
        # Render a simple horizontal bar chart
        df_counts = pd.DataFrame({
            "Class Name": [c.title() for c in counts.keys()],
            "Image Count": list(counts.values())
        })
        st.bar_chart(df_counts, x="Class Name", y="Image Count")

    st.divider()
    
    # Training wizard step-by-step
    st.markdown(f"""
    <div class="flex-header">
        {get_svg_icon("settings", size=28, color="var(--theme-primary)")}
        <h3 style="color: var(--theme-green-dark); font-weight: 600;">Training Setup Wizard</h3>
    </div>
    """, unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown(f"""
        <div class="premium-card" style="height: 100%;">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 0.5rem;">
                {get_svg_icon("cpu", size=20, color="var(--theme-primary)")}
                <h4 style="color: var(--theme-green-dark); margin: 0;">Step 1: Hyperparameters</h4>
            </div>
            <p style="font-size: 0.9rem; color: var(--theme-text-muted); margin-bottom: 1rem;">Configure training complexity and optimization cycles.</p>
        """, unsafe_allow_html=True)
        
        epochs = st.number_input("Number of Epochs", min_value=1, max_value=100, value=10, 
                                 help="An epoch represents one full pass through the entire dataset. More epochs improve learning but take longer.")
        
        st.markdown("</div>", unsafe_allow_html=True)
            
    with col2:
        st.markdown(f"""
        <div class="premium-card" style="height: 100%;">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 0.5rem;">
                {get_svg_icon("settings", size=20, color="var(--theme-primary)")}
                <h4 style="color: var(--theme-green-dark); margin: 0;">Step 2: Execution Settings</h4>
            </div>
            <p style="font-size: 0.9rem; color: var(--theme-text-muted); margin-bottom: 1rem;">Choose how training runs on your machine.</p>
        """, unsafe_allow_html=True)
        
        run_in_app = st.checkbox("Run synchronously inside app (blocks user actions)", value=False)
        st.info("💡 Background training lets you browse the app while training. Log updates will stream into the terminal console below.")
        st.markdown("</div>", unsafe_allow_html=True)

    st.write("")
    
    # Step 3: Run Training button
    if st.button("Start Model Training", type="primary", use_container_width=True):
        if total_images == 0:
            st.warning("Your dataset is currently empty. Please run 'Sync / Verify Dataset' above first.")
            download_dataset_if_missing()
        
        if run_in_app:
            st.write("Training model synchronously (please do not close this window)...")
            from app.model import train_model_pipeline
            try:
                model, history = train_model_pipeline(DATA_DIR, epochs=epochs)
                st.success("Model trained successfully and saved to models/garbage_model.keras!")
                try:
                    ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
                    subprocess.run([sys.executable, os.path.join(ROOT, 'scripts', 'plot_history.py')], check=True)
                except Exception as pe:
                    st.warning(f"Could not generate performance plot: {pe}")
            except Exception as e:
                st.error(f"Error during training: {e}")
        else:
            ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
            logs_dir = os.path.join(ROOT, 'logs')
            os.makedirs(logs_dir, exist_ok=True)
            log_file_path = os.path.join(logs_dir, 'training.log')
            # Open in write mode to clear previous logs when a new training runs
            log_file = open(log_file_path, 'w', encoding='utf-8')
            cmd = [sys.executable, os.path.join(ROOT, 'scripts', 'train.py'), '--epochs', str(epochs)]
            proc = subprocess.Popen(cmd, cwd=ROOT, stdout=log_file, stderr=subprocess.STDOUT)
            st.session_state['training_pid'] = proc.pid
            st.success(f"Training process started in background. (Process PID: {proc.pid})")

    # Display background tasks and monitoring
    pid = st.session_state.get('training_pid')
    if pid:
        st.divider()
        st.markdown(f"""
        <div class="flex-header">
            {get_svg_icon("cpu", size=24, color="var(--theme-primary)")}
            <h4 style="color: var(--theme-green-dark); font-weight: 600; margin: 0;">Background Tasks Monitor</h4>
        </div>
        """, unsafe_allow_html=True)
        def is_running(pid):
            try:
                import os
                os.kill(pid, 0)
                return True
            except Exception:
                try:
                    import psutil
                    return psutil.pid_exists(pid)
                except Exception:
                    return False

        if is_running(pid):
            col_stat, col_act = st.columns([3, 1])
            with col_stat:
                st.info(f"⏳ Training process (PID: {pid}) is active and executing epochs...")
            with col_act:
                if st.button("Terminate Training", use_container_width=True, type="primary"):
                    try:
                        if os.name == 'nt':
                            subprocess.check_call(["taskkill", "/PID", str(pid), "/F"])
                        else:
                            os.kill(pid, 9)
                        st.success(f"Stopped process {pid}.")
                        del st.session_state['training_pid']
                        st.rerun()
                    except Exception as e:
                        st.error(f"Failed to terminate process {pid}: {e}")
        else:
            st.warning("Background task finished or stopped. Logging history finalized.")
            del st.session_state['training_pid']

    st.divider()
    st.markdown(f"""
    <div class="flex-header">
        {get_svg_icon("terminal", size=28, color="var(--theme-primary)")}
        <h3 style="color: var(--theme-green-dark); font-weight: 600;">Training Logs Output Console</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Styled logs refreshing console
    col_log_header, col_log_refresh = st.columns([4, 1])
    with col_log_header:
        st.write("Active log stream from `logs/training.log`:")
    with col_log_refresh:
        btn_refresh = st.button("Refresh Logs Stream", use_container_width=True)

    log_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')), 'logs', 'training.log')
    if os.path.exists(log_path):
        with open(log_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()[-100:]
        
        # Build styled console
        console_html = '<div class="terminal-console">'
        for line in lines:
            if "Epoch" in line:
                console_html += f'<span class="terminal-line-success">{line}</span><br/>'
            elif "INFO" in line or "Saved" in line:
                console_html += f'<span class="terminal-line-info">{line}</span><br/>'
            else:
                console_html += f'{line}<br/>'
        console_html += '</div>'
        st.markdown(console_html, unsafe_allow_html=True)
    else:
        st.write("No active logs available. Start training to initialize log output.")

    # Render training performance plot if available
    ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    plot_path = os.path.join(ROOT, 'logs', 'training_plot.png')
    if os.path.exists(plot_path):
        st.divider()
        st.markdown(f"""
        <div class="flex-header">
            {get_svg_icon("chart", size=28, color="var(--theme-primary)")}
            <h3 style="color: var(--theme-green-dark); font-weight: 600;">Training Results & Performance Curves</h3>
        </div>
        """, unsafe_allow_html=True)
        st.image(plot_path, use_column_width=True, caption="Training metrics showing accuracy and loss progression.")

if __name__ == "__main__":
    main()