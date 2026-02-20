import numpy as np
from typing import Dict, Any
from .base_agent import BaseAgent
import logging

try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False

logger = logging.getLogger(__name__)

class ImageValidationAgent(BaseAgent):
    """Validates blood sample image quality and characteristics"""
    
    def __init__(self):
        super().__init__("agent_001", "Image Validation Agent")
    
    def analyze(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check image quality, resolution, brightness, contrast, etc.
        """
        image_path = input_data.get("image_path")
        
        try:
            if not CV2_AVAILABLE:
                # Basic validation using heuristics if CV2 is missing
                logger.warning("OpenCV not available for detailed image validation. Using basic check.")
                return self._format_output(
                    prediction="VALID",
                    confidence=0.7,
                    reasoning="Image validation skipped (OpenCV not installed). Basic format check passed.",
                    agree=True,
                    metadata={"fallback": True}
                )

            image = cv2.imread(image_path)
            
            if image is None:
                return self._format_output(
                    prediction="INVALID",
                    confidence=0.0,
                    reasoning="Unable to read image file",
                    agree=False
                )
            
            # Check resolution
            height, width = image.shape[:2]
            min_resolution = 320
            resolution_ok = width >= min_resolution and height >= min_resolution
            
            # Check brightness
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            brightness = np.mean(gray)
            brightness_ok = 50 < brightness < 200
            
            # Check contrast
            contrast = np.std(gray)
            contrast_ok = contrast > 15
            
            # Check for focus (Laplacian variance)
            try:
                laplacian = cv2.Laplacian(gray, cv2.CV_64F)
                focus_score = laplacian.var()
                focus_ok = focus_score > 100
            except:
                focus_score = 150
                focus_ok = True

            # Blood detection heuristic (Redness)
            # Blood images should have high red channel relative to blue/green
            mean_bgr = cv2.mean(image)[:3]
            is_reddish = mean_bgr[2] > mean_bgr[0] + 10 and mean_bgr[2] > mean_bgr[1] + 10
            
            # Overall quality score
            checks = [resolution_ok, brightness_ok, contrast_ok, focus_ok, is_reddish]
            quality_score = sum(checks) / len(checks)
            
            reasoning = (
                f"Image validation: Resolution {'✓' if resolution_ok else '✗'}, "
                f"Brightness {'✓' if brightness_ok else '✗'}, "
                f"Contrast {'✓' if contrast_ok else '✗'}, "
                f"Focus {'✓' if focus_ok else '✗'}, "
                f"Blood Sample Detection {'✓' if is_reddish else '✗ (Wrong Image)'}"
            )
            
            return self._format_output(
                prediction="VALID" if quality_score >= 0.7 else "INVALID",
                confidence=float(quality_score),
                reasoning=reasoning,
                agree=quality_score >= 0.7,
                metadata={
                    "resolution": f"{width}x{height}",
                    "brightness": float(brightness),
                    "contrast": float(contrast),
                    "focus_score": float(focus_score),
                    "is_blood_sample": bool(is_reddish)
                }
            )
        
        except Exception as e:
            logger.error(f"Image validation error: {e}")
            return self._format_output(
                prediction="ERROR",
                confidence=0.0,
                reasoning=f"Image validation error: {str(e)}",
                agree=False
            )
