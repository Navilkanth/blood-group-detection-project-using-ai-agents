import numpy as np
from typing import Dict, Any, List
from .base_agent import BaseAgent

class ConfidenceAssessmentAgent(BaseAgent):
    """Assesses overall confidence and uncertainty in predictions"""
    
    def __init__(self):
        super().__init__("agent_004", "Confidence Assessment Agent")
    
    def analyze(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate confidence metrics based on agent disagreement and data quality
        """
        agent_predictions = input_data.get("agent_predictions", [])
        image_quality = input_data.get("image_quality", 0.5)
        
        try:
            if not agent_predictions:
                return self._format_output(
                    prediction="INSUFFICIENT_DATA",
                    confidence=0.0,
                    reasoning="No agent predictions available",
                    agree=False
                )
            
            # Calculate consensus score
            predictions = [a.get("prediction") for a in agent_predictions if a.get("prediction")]
            confidences = [a.get("confidence", 0.5) for a in agent_predictions]
            
            # Agreement ratio
            unique_predictions = set(predictions)
            agreement_ratio = 1.0 - (len(unique_predictions) - 1) / max(len(agent_predictions), 1)
            
            # Average confidence
            avg_confidence = np.mean(confidences)
            
            # Combined confidence score
            combined_confidence = (
                0.5 * agreement_ratio +
                0.3 * avg_confidence +
                0.2 * image_quality
            )
            
            # Assessment level
            if combined_confidence >= 0.85:
                assessment = "HIGH"
            elif combined_confidence >= 0.70:
                assessment = "MODERATE"
            elif combined_confidence >= 0.50:
                assessment = "LOW"
            else:
                assessment = "VERY_LOW"
            
            reasoning = (
                f"Confidence assessment: {assessment}. "
                f"Agent agreement: {agreement_ratio:.0%}, "
                f"Average confidence: {avg_confidence:.0%}, "
                f"Image quality: {image_quality:.0%}"
            )
            
            return self._format_output(
                prediction=assessment,
                confidence=combined_confidence,
                reasoning=reasoning,
                agree=combined_confidence >= 0.70,
                metadata={
                    "agreement_ratio": float(agreement_ratio),
                    "average_confidence": float(avg_confidence),
                    "image_quality_score": float(image_quality),
                    "unique_predictions": len(unique_predictions),
                }
            )
        
        except Exception as e:
            return self._format_output(
                prediction="ERROR",
                confidence=0.0,
                reasoning=f"Confidence assessment error: {str(e)}",
                agree=False
            )
