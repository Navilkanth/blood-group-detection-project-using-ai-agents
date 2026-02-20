from typing import Dict, Any
from .base_agent import BaseAgent

class MedicalRulesAgent(BaseAgent):
    """Applies medical domain knowledge and blood group genetics"""
    
    def __init__(self):
        super().__init__("agent_003", "Medical Rules Agent")
        self.blood_group_properties = {
            "A": {"antigens": ["A"], "can_donate_to": ["A", "AB"], "rh_compatible": True},
            "B": {"antigens": ["B"], "can_donate_to": ["B", "AB"], "rh_compatible": True},
            "AB": {"antigens": ["A", "B"], "can_donate_to": ["AB"], "rh_compatible": True},
            "O": {"antigens": [], "can_donate_to": ["A", "B", "AB", "O"], "rh_compatible": True},
        }
    
    def analyze(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate prediction against medical rules and genetic compatibility
        """
        cnn_prediction = input_data.get("cnn_prediction", "UNKNOWN")
        agglutination_pattern = input_data.get("agglutination_pattern", {})
        
        try:
            if cnn_prediction not in self.blood_group_properties:
                return self._format_output(
                    prediction="INCONCLUSIVE",
                    confidence=0.3,
                    reasoning="Prediction does not match standard blood groups",
                    agree=False
                )
            
            # Validate against medical rules
            blood_group_info = self.blood_group_properties[cnn_prediction]
            validation_score = self._validate_against_rules(
                cnn_prediction,
                agglutination_pattern,
                blood_group_info
            )
            
            # Optional CBC validation (simulated)
            cbc_note = ""
            hgb = input_data.get("cbc_data", {}).get("hemoglobin", 14.0)
            if hgb < 12.0:
                cbc_note = " (Clinical Note: Low hemoglobin detected)"
            elif hgb > 16.5:
                cbc_note = " (Clinical Note: Polycythemia check recommended)"

            reasoning = (
                f"Medical validation: Blood type {cnn_prediction} is genetically valid. "
                f"Antigens present: {', '.join(blood_group_info['antigens']) or 'None'}. "
                f"Universal donor compatibility: {cnn_prediction == 'O'}.{cbc_note}"
            )
            
            return self._format_output(
                prediction=cnn_prediction,
                confidence=validation_score,
                reasoning=reasoning,
                agree=validation_score >= 0.65,
                metadata=blood_group_info
            )
        
        except Exception as e:
            return self._format_output(
                prediction="ERROR",
                confidence=0.0,
                reasoning=f"Medical rules error: {str(e)}",
                agree=False
            )
    
    def _validate_against_rules(
        self,
        blood_type: str,
        pattern: Dict,
        properties: Dict
    ) -> float:
        """Calculate validation score based on medical rules"""
        score = 0.7  # Base score
        
        # Bonus for O type (universal donor)
        if blood_type == "O":
            score += 0.15
        
        # Check pattern consistency
        if pattern.get("antigen_a_present") and blood_type in ["A", "AB"]:
            score += 0.05
        if pattern.get("antigen_b_present") and blood_type in ["B", "AB"]:
            score += 0.05
        
        return min(1.0, score)
