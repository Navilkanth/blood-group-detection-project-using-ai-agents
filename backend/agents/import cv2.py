import cv2
import numpy as np
from typing import Dict, Any, Tuple
from .base_agent import BaseAgent
from models.model_manager import ModelManager
from models.model_config import BLOOD_TYPE_MAPPING, CONFIDENCE_CALIBRATION
import logging

logger = logging.getLogger(__name__)

class AgglutinationDetectionAgent(BaseAgent):
    """Detects blood type patterns using CNN model"""
    
    def __init__(self, model_path: str = None):
        super().__init__("agent_002", "Agglutination Detection Agent")
        self.blood_types = ["A", "B", "AB", "O"]
        self.model_path = model_path
        self.model_manager = ModelManager()
        self.model = None
        
        # Load model if path provided
        if model_path:
            try:
                self.model = self.model_manager.load_model(model_path)
                logger.info("CNN model loaded successfully")
            except Exception as e:
                logger.warning(f"Could not load CNN model: {e}. Falling back to heuristics.")
                self.model = None
    
    def analyze(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze blood sample image using CNN model for agglutination patterns
        """
        image_path = input_data.get("image_path")
        
        try:
            # Read image
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError("Unable to read image file")
            
            # Convert BGR to RGB for model
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Use CNN model if available
            if self.model:
                prediction, confidence, metadata = self._predict_with_cnn(image_rgb)
            else:
                # Fallback to heuristics
                logger.warning("Using heuristic prediction (CNN not available)")
                prediction, confidence, metadata = self._predict_with_heuristics(image_rgb)
            
            # Apply confidence calibration
            calibrated_confidence = self._calibrate_confidence(prediction, confidence)
            
            reasoning = (
                f"CNN agglutination analysis detected blood type: {prediction} "
                f"(raw confidence: {confidence:.2%}, calibrated: {calibrated_confidence:.2%}). "
                f"Detection method: {'PyTorch CNN' if self.model else 'Heuristic Fallback'}"
            )
            
            return self._format_output(
                prediction=prediction,
                confidence=calibrated_confidence,
                reasoning=reasoning,
                agree=calibrated_confidence >= 0.65,
                metadata={
                    **metadata,
                    "detection_method": "CNN" if self.model else "heuristic",
                    "raw_confidence": confidence,
                    "calibrated_confidence": calibrated_confidence,
                }
            )
        
        except Exception as e:
            logger.error(f"Agglutination detection error: {str(e)}")
            return self._format_output(
                prediction="UNKNOWN",
                confidence=0.0,
                reasoning=f"Agglutination detection error: {str(e)}",
                agree=False
            )
    
    def _predict_with_cnn(self, image_array: np.ndarray) -> Tuple[str, float, Dict]:
        """
        Use CNN model for prediction
        
        Args:
            image_array: RGB image as numpy array
            
        Returns:
            (blood_type, confidence, metadata)
        """
        try:
            # Preprocess image
            image_tensor = self.model_manager.preprocess_image(image_array)
            
            # Run inference
            inference_result = self.model_manager.inference(self.model, image_tensor)
            
            primary = inference_result["primary_prediction"]
            blood_type = primary["blood_type"]
            confidence = primary["confidence"]
            
            # Collect metadata
            metadata = {
                "top_predictions": [
                    {
                        "blood_type": p["blood_type"],
                        "confidence": p["confidence"]
                    }
                    for p in inference_result["top_predictions"]
                ],
                "model_output_shape": inference_result["raw_logits"].shape,
            }
            
            return blood_type, confidence, metadata
        
        except Exception as e:
            logger.error(f"CNN inference failed: {e}")
            raise
    
    def _predict_with_heuristics(self, image_rgb: np.ndarray) -> Tuple[str, float, Dict]:
        """
        Fallback heuristic-based prediction using image features
        
        Args:
            image_rgb: RGB image as numpy array
            
        Returns:
            (blood_type, confidence, metadata)
        """
        # Convert to grayscale for analysis
        gray = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)
        
        # Analyze color channels
        red_mean = np.mean(image_rgb[:, :, 0])
        green_mean = np.mean(image_rgb[:, :, 1])
        blue_mean = np.mean(image_rgb[:, :, 2])
        
        # Detect edges (agglutination patterns)
        edges = cv2.Canny(gray, 100, 200)
        edge_density = np.sum(edges > 0) / (edges.shape[0] * edges.shape[1])
        
        # Analyze histogram
        hist_blue = cv2.calcHist([image_rgb], [0], None, [256], [0, 256])
        hist_red = cv2.calcHist([image_rgb], [2], None, [256], [0, 256])
        
        # Simple heuristic rules
        color_score_o = max(0, red_mean - 30)  # O type shows more red
        color_score_a = max(0, green_mean - 20)  # A shows more green
        color_score_b = max(0, blue_mean - 20)  # B shows more blue
        color_score_ab = (green_mean + blue_mean) / 2  # AB mixed
        
        scores = {
            "O": color_score_o + edge_density * 50,
            "A": color_score_a + edge_density * 45,
            "B": color_score_b + edge_density * 42,
            "AB": color_score_ab + edge_density * 40,
        }
        
        blood_type = max(scores, key=scores.get)
        confidence = scores[blood_type] / 100  # Normalize to 0-1
        confidence = min(1.0, confidence)
        
        metadata = {
            "channel_means": {
                "red": float(red_mean),
                "green": float(green_mean),
                "blue": float(blue_mean),
            },
            "edge_density": float(edge_density),
            "heuristic_scores": {k: float(v) for k, v in scores.items()},
        }
        
        return blood_type, confidence, metadata
    
    def _calibrate_confidence(self, blood_type: str, raw_confidence: float) -> float:
        """
        Calibrate confidence based on blood type difficulty
        
        Args:
            blood_type: Predicted blood type
            raw_confidence: Raw model confidence
            
        Returns:
            Calibrated confidence score
        """
        # Apply blood-type specific calibration
        calibration_factor = CONFIDENCE_CALIBRATION.get(blood_type, 0.70)
        
        # Adjust confidence based on calibration threshold
        if raw_confidence >= calibration_factor:
            # Increase confidence for high predictions
            calibrated = 0.7 + (raw_confidence - calibration_factor) * 0.3
        else:
            # Reduce confidence for low predictions
            calibrated = raw_confidence * (calibration_factor / 1.0)
        
        return min(1.0, max(0.0, calibrated))
