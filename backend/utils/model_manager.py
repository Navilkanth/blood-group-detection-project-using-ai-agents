"""
Centralized Model Management Utility
Handles all model loading, path resolution, and label management
"""

import os
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class ModelManager:
    """Centralized model and label management"""
    
    # Define model and label paths relative to project structure
    PROJECT_ROOT = Path(__file__).parent.parent.parent
    MODELS_DIR = PROJECT_ROOT / "backend" / "models"
    MODEL_NAME = "blood_model_FIXED.keras"  # Prioritize keras format (trained model)
    LABEL_NAME = "MODEL LABEL.json"
    
    # Fallback paths - Keras format prioritized
    FALLBACK_PATHS = [
        PROJECT_ROOT / "backend" / "models" / MODEL_NAME,       # Keras in models folder
        PROJECT_ROOT / MODEL_NAME,                                # Keras in root
        PROJECT_ROOT / ".." / MODEL_NAME,                       # One level up
        Path.home() / "Downloads" / MODEL_NAME,                 # Keras in downloads
    ]
    
    # Default blood group classes (if labels file is not found)
    DEFAULT_LABELS = ["A", "AB", "B", "O"]
    
    # Cache for model and labels
    _model_cache = None
    _labels_cache = None
    _model_path = None
    _labels_path = None
    
    @classmethod
    def get_model_path(cls):
        """
        Get the correct model path, checking multiple locations
        Uses trained keras model format
        Returns the first existing model file
        """
        if cls._model_path and os.path.exists(cls._model_path):
            return cls._model_path
        
        # Check primary location (backend/models)
        if cls.MODELS_DIR.exists():
            model_file = cls.MODELS_DIR / cls.MODEL_NAME
            if model_file.exists():
                cls._model_path = str(model_file)
                logger.info(f"Model found at: {cls._model_path}")
                return cls._model_path
        
        # Check fallback paths
        for fallback_path in cls.FALLBACK_PATHS:
            if fallback_path.exists():
                cls._model_path = str(fallback_path)
                logger.info(f"Model found at fallback path: {cls._model_path}")
                return cls._model_path
        
        logger.error(f"Model file not found! Searched in: {cls.MODELS_DIR}, {cls.FALLBACK_PATHS}")
        raise FileNotFoundError(f"Trained model '{cls.MODEL_NAME}' not found in any expected location")
    
    @classmethod
    def get_labels_path(cls):
        """
        Get the correct labels path, checking multiple locations
        Returns the first existing labels file
        """
        if cls._labels_path and os.path.exists(cls._labels_path):
            return cls._labels_path
        
        # Check primary location
        if cls.MODELS_DIR.exists():
            labels_file = cls.MODELS_DIR / cls.LABEL_NAME
            if labels_file.exists():
                cls._labels_path = str(labels_file)
                logger.info(f"Labels found at: {cls._labels_path}")
                return cls._labels_path
        
        # Check root Downloads
        root_labels = cls.PROJECT_ROOT / cls.LABEL_NAME
        if root_labels.exists():
            cls._labels_path = str(root_labels)
            logger.info(f"Labels found at: {cls._labels_path}")
            return cls._labels_path
        
        logger.warning(f"Labels file not found! Will use default labels: {cls.DEFAULT_LABELS}")
        return None
    
    @classmethod
    def load_labels(cls):
        """
        Load blood group labels from JSON file or use defaults
        Returns list of blood group class names
        """
        if cls._labels_cache is not None:
            return cls._labels_cache
        
        labels_path = cls.get_labels_path()
        
        if labels_path and os.path.exists(labels_path):
            try:
                with open(labels_path, 'r') as f:
                    cls._labels_cache = json.load(f)
                    logger.info(f"Loaded {len(cls._labels_cache)} blood group labels")
                    return cls._labels_cache
            except Exception as e:
                logger.error(f"Error loading labels from {labels_path}: {e}")
                logger.warning("Using default labels instead")
        
        cls._labels_cache = cls.DEFAULT_LABELS.copy()
        return cls._labels_cache
    
    @classmethod
    def load_model(cls):
        """
        Lazy load the trained TensorFlow/Keras model
        Caches model in memory after first load
        """
        if cls._model_cache is not None:
            return cls._model_cache
        
        try:
            import tensorflow as tf
        except ImportError:
            logger.error("TensorFlow is not installed!")
            raise ImportError("TensorFlow is required to load the model")
        
        model_path = cls.get_model_path()
        
        try:
            logger.info(f"Loading trained model from: {model_path}")
            cls._model_cache = tf.keras.models.load_model(model_path)
            logger.info(f"✓ Model loaded successfully!")
            logger.info(f"  Input shape: {cls._model_cache.input_shape}")
            logger.info(f"  Output shape: {cls._model_cache.output_shape}")
            return cls._model_cache
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise
    
    @classmethod
    def predict(cls, image_array):
        """
        Make a prediction on a preprocessed image array
        
        Args:
            image_array: Preprocessed numpy array of shape (1, 224, 224, 3)
        
        Returns:
            dict with keys: blood_group, confidence, all_predictions
        """
        model = cls.load_model()
        labels = cls.load_labels()
        
        try:
            predictions = model.predict(image_array, verbose=0)
            predicted_class = int(predictions.argmax())
            confidence = float(predictions[0][predicted_class])
            
            return {
                'blood_group': labels[predicted_class],
                'confidence': confidence,
                'all_predictions': {labels[i]: float(predictions[0][i]) for i in range(len(labels))}
            }
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            raise
    
    @classmethod
    def clear_cache(cls):
        """Clear cached model and labels (useful for reloading)"""
        cls._model_cache = None
        cls._labels_cache = None
        cls._model_path = None
        cls._labels_path = None
        logger.info("Model cache cleared")
    
    @classmethod
    def get_status(cls):
        """Get status information about model and labels"""
        status = {
            'model_found': False,
            'labels_found': False,
            'model_path': None,
            'labels_path': None,
            'labels': None
        }
        
        try:
            status['model_path'] = cls.get_model_path()
            status['model_found'] = True
        except FileNotFoundError:
            status['model_found'] = False
        
        labels_path = cls.get_labels_path()
        if labels_path:
            status['labels_path'] = labels_path
            status['labels_found'] = True
        
        try:
            status['labels'] = cls.load_labels()
        except Exception as e:
            status['labels'] = cls.DEFAULT_LABELS
        
        return status
