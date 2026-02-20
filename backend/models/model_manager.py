"""
Model Manager - Handles CNN model lifecycle and inference
"""
import torch
import torch.nn as nn
import os
from typing import Tuple, Dict, Any
import logging
from .model_config import (
    MODEL_ARCHITECTURE,
    BLOOD_TYPE_MAPPING,
    INFERENCE_SETTINGS
)

logger = logging.getLogger(__name__)

class ModelManager:
    """Manages CNN model loading, caching, and inference"""
    
    _instance = None
    _models_cache = {}
    
    def __new__(cls):
        """Singleton pattern for model manager"""
        if cls._instance is None:
            cls._instance = super(ModelManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize model manager"""
        if self._initialized:
            return
        
        self.device = torch.device("cuda" if (
            torch.cuda.is_available() and 
            INFERENCE_SETTINGS["use_gpu"]
        ) else "cpu")
        
        self._initialized = True
        logger.info(f"ModelManager initialized on device: {self.device}")
    
    def load_model(self, model_path: str, force_reload: bool = False) -> nn.Module:
        """
        Load CNN model with caching
        
        Args:
            model_path: Path to trained model file (.pth or .pt)
            force_reload: Force reload even if cached
            
        Returns:
            Loaded PyTorch model
        """
        if model_path in self._models_cache and not force_reload:
            logger.info(f"Loading model from cache: {model_path}")
            return self._models_cache[model_path]
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
        
        try:
            logger.info(f"Loading model from disk: {model_path}")
            model = torch.load(model_path, map_location=self.device)
            model.eval()  # Set to evaluation mode
            
            # Disable gradients for inference
            for param in model.parameters():
                param.requires_grad = False
            
            self._models_cache[model_path] = model
            logger.info(f"Model loaded successfully")
            
            return model
        
        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            raise
    
    def preprocess_image(self, image_array) -> torch.Tensor:
        """
        Preprocess image for model input
        
        Args:
            image_array: PIL Image or numpy array
            
        Returns:
            Preprocessed torch tensor
        """
        import torchvision.transforms as transforms
        from PIL import Image
        import numpy as np
        
        # Convert to PIL if numpy array
        if isinstance(image_array, np.ndarray):
            image_array = Image.fromarray(image_array)
        
        # Define preprocessing pipeline
        preprocess = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])
        
        tensor = preprocess(image_array)
        return tensor.unsqueeze(0).to(self.device)  # Add batch dimension
    
    def inference(self, model: nn.Module, image_tensor: torch.Tensor) -> Dict[str, Any]:
        """
        Run inference on preprocessed image
        
        Args:
            model: PyTorch model
            image_tensor: Preprocessed image tensor
            
        Returns:
            Predictions with confidence scores
        """
        try:
            with torch.no_grad():
                outputs = model(image_tensor)
            
            # Get probabilities
            probabilities = torch.softmax(outputs, dim=1)
            
            # Get top predictions
            top_k = INFERENCE_SETTINGS.get("top_k_predictions", 2)
            top_probs, top_indices = torch.topk(probabilities, top_k, dim=1)
            
            predictions = []
            for prob, idx in zip(top_probs[0], top_indices[0]):
                blood_type = BLOOD_TYPE_MAPPING.get(idx.item(), "UNKNOWN")
                predictions.append({
                    "blood_type": blood_type,
                    "confidence": prob.item(),
                    "class_index": idx.item(),
                })
            
            return {
                "primary_prediction": predictions[0],
                "top_predictions": predictions,
                "raw_logits": outputs.cpu().numpy(),
                "all_probabilities": probabilities.cpu().numpy(),
            }
        
        except Exception as e:
            logger.error(f"Inference failed: {str(e)}")
            raise
    
    def get_device(self) -> torch.device:
        """Get current device"""
        return self.device
    
    def clear_cache(self):
        """Clear model cache"""
        self._models_cache.clear()
        logger.info("Model cache cleared")
