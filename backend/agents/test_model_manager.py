"""
Tests for model manager and CNN inference
"""
import pytest
import numpy as np
from PIL import Image
from models.model_manager import ModelManager

class TestModelManager:
    """Test model manager functionality"""
    
    def test_singleton_pattern(self):
        """Test that ModelManager uses singleton pattern"""
        mm1 = ModelManager()
        mm2 = ModelManager()
        
        assert mm1 is mm2
    
    def test_device_detection(self):
        """Test device detection (CPU/GPU)"""
        mm = ModelManager()
        device = mm.get_device()
        
        assert device is not None
        assert "cpu" in str(device) or "cuda" in str(device)
    
    def test_preprocess_image_from_pil(self):
        """Test image preprocessing from PIL Image"""
        mm = ModelManager()
        
        # Create test image
        image = Image.new('RGB', (224, 224), color='red')
        tensor = mm.preprocess_image(image)
        
        assert tensor.shape[0] == 1  # Batch size
        assert tensor.shape[1] == 3  # Channels
        assert tensor.shape[2] == 224  # Height
        assert tensor.shape[3] == 224  # Width
    
    def test_preprocess_image_from_numpy(self):
        """Test image preprocessing from numpy array"""
        mm = ModelManager()
        
        # Create test image array
        image_array = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
        tensor = mm.preprocess_image(image_array)
        
        assert tensor.shape[0] == 1
        assert tensor.shape[1] == 3
    
    def test_cache_management(self, tmp_path):
        """Test model cache management"""
        mm = ModelManager()
        initial_cache_size = len(mm._models_cache)
        
        mm.clear_cache()
        assert len(mm._models_cache) == 0
    
    def test_load_nonexistent_model(self):
        """Test error handling for nonexistent model"""
        mm = ModelManager()
        
        with pytest.raises(FileNotFoundError):
            mm.load_model("/nonexistent/model.pth")
