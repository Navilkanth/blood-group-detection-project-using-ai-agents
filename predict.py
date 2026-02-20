import numpy as np
import os
import sys
from pathlib import Path

# Add backend to path for imports
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from utils.model_manager import ModelManager

def predict_blood_group(image_path):
    """
    Predict blood group from image using centralized model manager
    
    Args:
        image_path: Path to the blood group image file
    
    Returns:
        dict with keys: blood_group, confidence, all_predictions
    """
    try:
        # Validate image path
        if not os.path.exists(image_path):
            return {'error': f'Image file not found: {image_path}'}
        
        # Load and preprocess image
        img = image.load_img(image_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)
        
        # Make prediction using model manager
        result = ModelManager.predict(img_array)
        return result
        
    except Exception as e:
        return {'error': str(e)}

if __name__ == "__main__":
    # Check model status
    print("=" * 60)
    print("BLOOD GROUP MODEL STATUS")
    print("=" * 60)
    status = ModelManager.get_status()
    print(f"Model Found: {status['model_found']}")
    print(f"Model Path: {status['model_path']}")
    print(f"Labels Found: {status['labels_found']}")
    print(f"Labels Path: {status['labels_path']}")
    print(f"Blood Group Classes: {status['labels']}")
    print("=" * 60)
    
    # Test prediction (requires actual image file)
    test_image = "path/to/test/image.jpg"
    if os.path.exists(test_image):
        result = predict_blood_group(test_image)
        print("\nPrediction Result:")
        print(result)
    else:
        print(f"\nNote: Test image '{test_image}' not found. Provide a valid image path to test predictions.")
