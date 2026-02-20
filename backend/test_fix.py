import os
import sys

# Crucial: This must be set BEFORE importing tensorflow
os.environ["TF_USE_LEGACY_KERAS"] = "1"

print("--- VERSION CHECK ---")
try:
    import tensorflow as tf
    print(f"TensorFlow Version: {tf.__version__}")
    
    # Try to import tf_keras to confirm legacy support exists
    try:
        import tf_keras
        print(f"Legacy Keras (tf-keras) found: {tf_keras.__version__}")
    except ImportError:
        print("⚠️ Warning: tf-keras package not found. Performance might be unpredictable.")

    from tensorflow.keras.models import load_model
    from backend.config import Config

    model_path = Config.get_model_path()
    print(f"Attempting to load: {model_path}")

    # Load the model
    model = load_model(model_path, compile=False)
    print("✅ SUCCESS: Model loaded perfectly without shape errors!")
    
except Exception as e:
    print(f"❌ FAILURE: {e}")
    if "shape" in str(e).lower():
        print("💡 Recommendation: Run 'pip install tf-keras' to fix the shape conversion issue.")
