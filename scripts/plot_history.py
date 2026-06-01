import pandas as pd
import matplotlib.pyplot as plt
import os

# Define paths
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
csv_path = os.path.join(ROOT, 'logs', 'training_history.csv')
plot_path = os.path.join(ROOT, 'logs', 'training_plot.png')

# Read history
if not os.path.exists(csv_path):
    print(f"Error: {csv_path} not found.")
    exit(1)

df = pd.read_csv(csv_path)

# Apply sleek styling
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Plot color palette
color_train_acc = '#1f77b4'  # Professional blue
color_val_acc = '#aec7e8'    # Light blue
color_train_loss = '#ff7f0e' # Vibrant orange
color_val_loss = '#ffbb78'   # Light orange

# 1. Accuracy Plot
ax1.plot(df['epoch'] + 1, df['accuracy'], label='Train Accuracy', color=color_train_acc, marker='o', linewidth=2)
ax1.plot(df['epoch'] + 1, df['val_accuracy'], label='Val Accuracy', color=color_val_acc, marker='s', linestyle='--', linewidth=2)
ax1.set_title('Model Classification Accuracy', fontsize=14, fontweight='bold', pad=15)
ax1.set_xlabel('Epoch', fontsize=11)
ax1.set_ylabel('Accuracy (Ratio)', fontsize=11)
ax1.set_xticks(df['epoch'] + 1)
ax1.set_ylim(0.5, 1.0)
ax1.legend(loc='lower right', frameon=True, facecolor='white', edgecolor='none', shadow=True)
ax1.grid(True, linestyle=':', alpha=0.6)

# 2. Loss Plot
ax2.plot(df['epoch'] + 1, df['loss'], label='Train Loss', color=color_train_loss, marker='o', linewidth=2)
ax2.plot(df['epoch'] + 1, df['val_loss'], label='Val Loss', color=color_val_loss, marker='s', linestyle='--', linewidth=2)
ax2.set_title('Sparse Categorical Cross-Entropy Loss', fontsize=14, fontweight='bold', pad=15)
ax2.set_xlabel('Epoch', fontsize=11)
ax2.set_ylabel('Loss Value', fontsize=11)
ax2.set_xticks(df['epoch'] + 1)
ax2.legend(loc='upper right', frameon=True, facecolor='white', edgecolor='none', shadow=True)
ax2.grid(True, linestyle=':', alpha=0.6)

# Main Title & Styling
plt.suptitle('AI Garbage Classifier Training Performance (Transfer Learning)', fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()

# Save plot to logs (for UI caching) and assets (for README documentation)
plot_path_assets = os.path.join(ROOT, 'assets', 'training_plot.png')
os.makedirs(os.path.dirname(plot_path_assets), exist_ok=True)

plt.savefig(plot_path, dpi=300, bbox_inches='tight')
plt.savefig(plot_path_assets, dpi=300, bbox_inches='tight')
print(f"[SUCCESS] Plot generated and saved to {plot_path} and {plot_path_assets}")
