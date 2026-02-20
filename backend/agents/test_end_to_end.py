"""
End-to-end integration tests
"""
import pytest
from backend.agents import (
    ImageValidationAgent,
    AgglutinationDetectionAgent,
    MedicalRulesAgent,
    ConfidenceAssessmentAgent,
    SafetyEthicsAgent,
)
from agents.consensus_engine import ConsensusEngine

class TestEndToEndAnalysis:
    """Test complete analysis pipeline"""
    
    def test_full_analysis_pipeline(self, test_image_path):
        """Test complete multi-agent analysis flow"""
        # Step 1: Image validation
        img_agent = ImageValidationAgent()
        img_result = img_agent.analyze({"image_path": test_image_path})
        assert img_result["prediction"] in ["VALID", "INVALID"]
        
        if img_result["prediction"] == "INVALID":
            pytest.skip("Test image validation failed")
        
        # Step 2: Agglutination detection
        agg_agent = AgglutinationDetectionAgent()
        agg_result = agg_agent.analyze({"image_path": test_image_path})
        assert agg_result["prediction"] in ["A", "B", "AB", "O"]
        
        # Step 3: Medical rules
        med_agent = MedicalRulesAgent()
        med_result = med_agent.analyze({
            "cnn_prediction": agg_result["prediction"],
            "agglutination_pattern": {}
        })
        assert med_result["prediction"] in ["A", "B", "AB", "O", "INCONCLUSIVE"]
        
        # Step 4: Confidence assessment
        conf_agent = ConfidenceAssessmentAgent()
        agent_outputs = [img_result, agg_result, med_result]
        conf_result = conf_agent.analyze({
            "agent_predictions": agent_outputs,
            "image_quality": img_result["confidence"]
        })
        
        # Step 5: Safety check
        safety_agent = SafetyEthicsAgent()
        safety_result = safety_agent.analyze({
            "agent_assessments": agent_outputs + [conf_result],
            "combined_confidence": conf_result["confidence"],
            "image_encrypted": True,
            "audit_logged": True
        })
        
        # Step 6: Consensus
        engine = ConsensusEngine()
        final_outputs = agent_outputs + [conf_result, safety_result]
        consensus = engine.process_multi_agent_analysis(final_outputs)
        
        assert consensus["consensus_prediction"] in ["A", "B", "AB", "O", "ERROR"]
        assert 0.0 <= consensus["consensus_confidence"] <= 1.0
        assert "reasoning" in consensus
    
    def test_analysis_with_disagreement(self, test_image_path):
        """Test pipeline when agents disagree"""
        img_agent = ImageValidationAgent()
        img_result = img_agent.analyze({"image_path": test_image_path})
        
        if img_result["prediction"] == "INVALID":
            pytest.skip("Test image validation failed")
        
        # Create manual outputs with disagreement
        outputs = [
            {"agent_id": "a1", "agent_name": "Agent 1", "prediction": "A", "confidence": 0.7},
            {"agent_id": "a2", "agent_name": "Agent 2", "prediction": "B", "confidence": 0.6},
            {"agent_id": "a3", "agent_name": "Agent 3", "prediction": "A", "confidence": 0.75},
        ]
        
        engine = ConsensusEngine()
        result = engine.process_multi_agent_analysis(outputs)
        
        # Should still reach consensus
        assert result["consensus_prediction"] is not None
        assert result["voting_ratio"] > 0  # Some agreement
