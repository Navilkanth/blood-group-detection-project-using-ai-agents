from typing import Dict, Any
from datetime import datetime
from .base_agent import BaseAgent
import logging

# Optional import for api_handler to prevent dependency loops or missing file crashes
try:
    from api_handler import BloodGroupAPI
except ImportError:
    BloodGroupAPI = None

logger = logging.getLogger(__name__)

class SafetyEthicsAgent(BaseAgent):
    """Ensures ethical use of blood group classification"""
    
    def __init__(self, model_path=None):
        super().__init__("agent_005", "Safety & Ethics Agent")
        self.confidence_threshold_for_deployment = 0.75
        self.max_confidence_threshold = 0.85
        self.disclaimer = "This is a diagnostic aid only, not a medical diagnosis"
        
        self.api = None
        if BloodGroupAPI and model_path:
            try:
                self.api = BloodGroupAPI(model_path)
            except Exception as e:
                logger.warning(f"Failed to initialize BloodGroupAPI in SafetyEthicsAgent: {e}")
    
    def analyze(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess safety, ethics, and deployment suitability of prediction
        """
        agent_assessments = input_data.get("agent_assessments", [])
        combined_confidence = input_data.get("combined_confidence", 0.0)
        image_encrypted = input_data.get("image_encrypted", False)
        audit_logged = input_data.get("audit_logged", False)
        
        try:
            # Safety checks
            confidence_safe = combined_confidence >= self.confidence_threshold_for_deployment
            compliance_safe = image_encrypted and audit_logged
            
            # Check for conflicting agent opinions
            predictions = [a.get("prediction") for a in agent_assessments if a.get("prediction")]
            unique_preds = set(predictions) - {"UNKNOWN", "ERROR", "INVALID"}
            conflicting_agents = len(unique_preds) > 1
            conflict_risk = "HIGH" if conflicting_agents else "LOW"
            
            # Overall safety assessment
            safety_score = (
                0.5 * (1.0 if confidence_safe else 0.0) +
                0.3 * (1.0 if compliance_safe else 0.0) +
                0.2 * (0.8 if not conflicting_agents else 0.5)
            )
            
            safe_for_deployment = safety_score >= 0.70
            
            reasoning = (
                f"Safety assessment: {'✓ SAFE' if safe_for_deployment else '⚠ CAUTION RECOMMENDED'}. "
                f"Confidence level {'adequate' if confidence_safe else 'below threshold'}, "
                f"Compliance {'verified' if compliance_safe else 'incomplete'}, "
                f"Agent conflict risk: {conflict_risk}. "
                f"Recommendation: {'Proceed with prediction' if safe_for_deployment else 'Request manual review'}"
            )
            
            return self._format_output(
                prediction="SAFE_FOR_DEPLOYMENT" if safe_for_deployment else "NEEDS_REVIEW",
                confidence=safety_score,
                reasoning=reasoning,
                agree=safe_for_deployment,
                metadata={
                    "confidence_threshold_met": confidence_safe,
                    "compliance_verified": compliance_safe,
                    "conflict_risk": conflict_risk,
                    "timestamp": datetime.now().isoformat(),
                }
            )
        
        except Exception as e:
            logger.error(f"Safety assessment error: {e}")
            return self._format_output(
                prediction="ERROR",
                confidence=0.0,
                reasoning=f"Safety assessment error: {str(e)}",
                agree=False
            )

    def validate_prediction(self, prediction_result):
        """Validate predictions meet ethical standards"""
        if 'error' in prediction_result:
            return False, "Error in prediction"
        
        confidence = prediction_result.get('confidence', 0)
        if confidence < 0.7:
            return False, "Confidence too low for reliable prediction"
        
        return True, self.disclaimer
    
    def log_prediction(self, prediction, is_valid):
        """Log predictions for audit trail"""
        # Implement logging logic
        pass
    
    def process_classification(self, image_path):
        """Process with safety checks"""
        logger.info(f"Processing: {image_path}")
        
        if not self.api:
            return {"error": "API handler not initialized"}
            
        # Get prediction
        result = self.api.classify_from_file(image_path)
        
        # Validate
        valid, msg = self.validate_prediction(result)
        
        if not valid:
            logger.warning(f"Validation failed: {msg}")
        
        return {
            'prediction': result,
            'validation': {'valid': valid, 'reason': msg}
        }
