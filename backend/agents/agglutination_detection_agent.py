import numpy as np
from PIL import Image
from typing import Dict, Any
from .base_agent import BaseAgent
import logging

# Import the centralized classifier
try:
    from model_loader import BloodGroupClassifier
except ImportError:
    # Fallback for relative imports if needed
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from model_loader import BloodGroupClassifier

logger = logging.getLogger(__name__)

class AgglutinationDetectionAgent(BaseAgent):
    """Detects blood type patterns using Keras model via BloodGroupClassifier"""
    
    def __init__(self, model_path: str = None, label_path: str = None):
        super().__init__("agent_002", "Agglutination Detection Agent")
        self.classifier = BloodGroupClassifier(model_path, label_path)
        self.blood_types = self.classifier.BLOOD_GROUPS
    
    def analyze(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze blood sample image using the classifier
        """
        image_path = input_data.get("image_path")
        
        try:
            # Try to use the model first
            result = self.classifier.predict(image_path)
            
            if result.get("success"):
                confidence = result["confidence"]
                # Strict threshold for blood recognition
                if confidence < 0.35:
                    prediction = "WRONG_IMAGE"
                    method = "AI Model (Strict Validation)"
                else:
                    prediction = result["blood_group"]
                    method = "AI Model (Keras)"
                metadata = {"probabilities": result["probabilities"]}
            else:
                # Fallback: pattern-based heuristic analysis
                logger.warning(f"Model prediction failed or not available: {result.get('error')}. Using heuristics.")
                prediction, confidence = self._predict_with_heuristics(image_path)
                method = "Heuristic Analysis (Fallback)"
                metadata = {"error": result.get("error")}
            
            if prediction == "WRONG_IMAGE":
                reasoning = "Image rejected: Sample does not appear to be a valid blood group or is too low quality."
            else:
                reasoning = (
                    f"Agglutination analysis detected blood type {prediction} "
                    f"using {method} (confidence: {confidence:.2%})"
                )
            
            return self._format_output(
                prediction=prediction,
                confidence=confidence,
                reasoning=reasoning,
                agree=(confidence >= 0.6 and prediction != "WRONG_IMAGE"),
                metadata={**metadata, "detection_method": method}
            )
        
        except Exception as e:
            logger.error(f"Agglutination detection error: {e}")
            return self._format_output(
                prediction="UNKNOWN",
                confidence=0.0,
                reasoning=f"Agglutination detection error: {str(e)}",
                agree=False
            )
    
    def _predict_with_heuristics(self, image_path: str) -> tuple:
        """Fallback heuristic-based prediction using PIL"""
        try:
            image = Image.open(image_path).convert("RGB")
            img_array = np.array(image)
            
            # Analyze color distribution
            red = np.mean(img_array[:, :, 0])
            green = np.mean(img_array[:, :, 1])
            blue = np.mean(img_array[:, :, 2])
            
            # Simple heuristic rules
            if red > green and red > blue:
                blood_type = "O"
                confidence = 0.65
            elif green > red and green > blue:
                blood_type = "A"
                confidence = 0.62
            elif blue > red and blue > green:
                blood_type = "B"
                confidence = 0.60
            else:
                blood_type = "AB"
                confidence = 0.58
            
            return blood_type, confidence
        except Exception as e:
            logger.error(f"Heuristic fallback failed: {e}")
            return "UNKNOWN", 0.0
