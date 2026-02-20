"""
Model Format Converter
Converts between different model formats (keras, h5, pth) for compatibility
"""

import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def convert_keras_to_h5(keras_path, output_h5_path=None):
    """
    Convert Keras .keras file to legacy .h5 format
    This can resolve compatibility issues with older TensorFlow versions
    """
    import tensorflow as tf
    
    if not os.path.exists(keras_path):
        raise FileNotFoundError(f"Keras model not found: {keras_path}")
    
    if output_h5_path is None:
        # Create output path with same name but .h5 extension
        output_h5_path = keras_path.replace('.keras', '.h5')
    
    try:
        logger.info(f"Loading model from: {keras_path}")
        model = tf.keras.models.load_model(keras_path)
        
        logger.info(f"Converting to H5 format...")
        model.save(output_h5_path)
        
        logger.info(f"Model successfully converted to: {output_h5_path}")
        return output_h5_path
    except Exception as e:
        logger.error(f"Conversion failed: {e}")
        raise

def try_load_model_with_fallback(model_path):
    """
    Try to load model with fallback strategies
    1. Try loading directly
    2. If .keras fails, try converting to h5
    3. Load from h5 if available
    """
    import tensorflow as tf
    
    model_path = str(model_path)
    logger.info(f"Attempting to load model: {model_path}")
    
    # Strategy 1: Try direct load
    try:
        logger.info("Strategy 1: Loading directly...")
        model = tf.keras.models.load_model(model_path)
        logger.info("✓ Model loaded successfully")
        return model
    except Exception as e:
        logger.warning(f"Direct load failed: {e}")
    
    # Strategy 2: Try converting .keras to .h5
    if model_path.endswith('.keras'):
        try:
            h5_path = model_path.replace('.keras', '.h5')
            if os.path.exists(h5_path):
                logger.info(f"Strategy 2: Loading existing H5 file...")
                model = tf.keras.models.load_model(h5_path)
                logger.info("✓ Model loaded from H5 successfully")
                return model
            else:
                logger.info(f"Strategy 2: Converting .keras to .h5...")
                h5_path = convert_keras_to_h5(model_path, h5_path)
                model = tf.keras.models.load_model(h5_path)
                logger.info("✓ Model loaded from converted H5 successfully")
                return model
        except Exception as e:
            logger.warning(f"H5 conversion strategy failed: {e}")
    
    # Strategy 3: Check for .h5 variant
    if model_path.endswith('.keras'):
        h5_path = model_path.replace('.keras', '.h5')
        if os.path.exists(h5_path):
            try:
                logger.info(f"Strategy 3: Loading H5 variant...")
                model = tf.keras.models.load_model(h5_path)
                logger.info("✓ Model loaded from H5 variant successfully")
                return model
            except Exception as e:
                logger.warning(f"H5 variant load failed: {e}")
    
    # If all strategies fail, raise the original error
    logger.error("All loading strategies failed")
    raise Exception(f"Could not load model from {model_path}")

if __name__ == "__main__":
    # Test conversion
    import sys
    
    if len(sys.argv) > 1:
        model_path = sys.argv[1]
        output_path = sys.argv[2] if len(sys.argv) > 2 else None
        
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        
        try:
            result = convert_keras_to_h5(model_path, output_path)
            print(f"Conversion successful: {result}")
        except Exception as e:
            print(f"Conversion failed: {e}")
            sys.exit(1)
    else:
        print("Usage: python convert_model.py <keras_model_path> [output_h5_path]")
