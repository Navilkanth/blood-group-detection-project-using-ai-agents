import sys
import os

print(f"Python Executable: {sys.executable}")
print(f"Python Path: {sys.path}")

try:
    import tensorflow as tf
    print(f"✅ TensorFlow Import Success!")
    print(f"TensorFlow Version: {tf.__version__}")
    from tensorflow.keras.models import load_model
    print(f"✅ Keras Import Success!")
except ImportError as e:
    print(f"❌ ImportError: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"❌ Unexpected Error: {e}")
    import traceback
    traceback.print_exc()
