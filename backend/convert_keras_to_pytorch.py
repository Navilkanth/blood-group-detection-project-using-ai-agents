"""
Convert Keras H5 model to PyTorch format
"""
import torch
import torch.nn as nn
from tensorflow.keras.models import load_model
import logging

logger = logging.getLogger(__name__)
from backend.config import Config


def convert_keras_to_pytorch(h5_model_path: str, output_pth_path: str):
    """
    Convert Keras model to PyTorch (wrapper approach)
    
    Note: Full conversion requires layer-by-layer mapping.
    This saves the model for inference with TensorFlow backend.
    """
    try:
        # Load Keras model
        print(f"Loading Keras model from {h5_model_path}...")
        keras_model = load_model(h5_model_path)
        
        # Save as PyTorch checkpoint
        checkpoint = {
            'model_state_dict': keras_model.get_weights(),
            'model_config': keras_model.get_config(),
            'framework': 'keras',
        }
        
        torch.save(checkpoint, output_pth_path)
        print(f"✅ Model saved to {output_pth_path}")
        print(f"Note: This preserves Keras model. For true PyTorch model, train using train_model.py")
        
    except Exception as e:
        logger.error(f"Conversion failed: {e}")
        raise


if __name__ == "__main__":
    convert_keras_to_pytorch(
        h5_model_path=Config.MODEL_PATHS.get("agglutination_cnn"),
        output_pth_path=r"C:\Users\navin\Downloads\BLOOD GROUP CLASSIFIACTION\backend\models\agglutination_model.pth"
    )
