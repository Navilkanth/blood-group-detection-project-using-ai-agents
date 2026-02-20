import torch
from tensorflow.keras.models import load_model
from pathlib import Path
from backend.config import Config

# Paths
h5_path = Config.MODEL_PATHS.get("agglutination_cnn")
pth_path = r"C:\Users\navin\Downloads\BLOOD GROUP CLASSIFIACTION\backend\models\agglutination_model.pth"

# Create output directory if it doesn't exist
Path(pth_path).parent.mkdir(parents=True, exist_ok=True)

# Load Keras model
print("Loading Keras model...")
keras_model = load_model(h5_path)
print("✅ Loaded")

# Save as PyTorch
print("Converting to PyTorch...")
torch.save({
    'model': keras_model,
    'type': 'keras_wrapped',
    'framework': 'tensorflow'
}, pth_path)

print(f"✅ Saved to: {pth_path}")
