"""
Unit tests for Blood Group Classification agents
"""
import pytest
from backend.agents import (
    ImageValidationAgent,
    AgglutinationDetectionAgent,
    MedicalRulesAgent,
    ConfidenceAssessmentAgent,
    SafetyEthicsAgent,
)

class TestImageValidationAgent:
    """Test image validation agent"""
    
    def test_initialization(self):
        """Test agent initialization"""
        agent = ImageValidationAgent()
        assert agent.agent_id == "agent_001"
        assert agent.agent_name == "Image Validation Agent"
    
    def test_valid_image_analysis(self, test_image_path):
        """Test analysis of valid image"""
        agent = ImageValidationAgent()
        result = agent.analyze({"image_path": test_image_path})
        
        assert "agent_id" in result
        assert "prediction" in result
        assert "confidence" in result
        assert "reasoning" in result
        assert 0.0 <= result["confidence"] <= 1.0
    
    def test_invalid_image_path(self):
        """Test handling of invalid image path"""
        agent = ImageValidationAgent()
        result = agent.analyze({"image_path": "/nonexistent/path/image.jpg"})
        
        assert result["prediction"] == "ERROR"
        assert result["confidence"] == 0.0
        assert result["agree"] == False

class TestAgglutinationDetectionAgent:
    """Test agglutination detection agent"""
    
    def test_initialization(self):
        """Test agent initialization"""
        agent = AgglutinationDetectionAgent()
        assert agent.agent_id == "agent_002"
        assert agent.agent_name == "Agglutination Detection Agent"
        assert agent.blood_types == ["A", "B", "AB", "O"]
    
    def test_heuristic_prediction(self, test_image_path):
        """Test heuristic-based prediction (no CNN model)"""
        agent = AgglutinationDetectionAgent(model_path=None)
        result = agent.analyze({"image_path": test_image_path})
        
        assert result["prediction"] in ["A", "B", "AB", "O", "UNKNOWN"]
        assert 0.0 <= result["confidence"] <= 1.0
        assert result["metadata"]["detection_method"] == "heuristic"

class TestMedicalRulesAgent:
    """Test medical rules agent"""
    
    def test_initialization(self):
        """Test agent initialization"""
        agent = MedicalRulesAgent()
        assert agent.agent_id == "agent_003"
        assert agent.agent_name == "Medical Rules Agent"
        assert len(agent.blood_group_properties) == 4
    
    def test_blood_type_a_validation(self):
        """Test A blood type validation"""
        agent = MedicalRulesAgent()
        result = agent.analyze({
            "cnn_prediction": "A",
            "agglutination_pattern": {}
        })
        
        assert result["prediction"] == "A"
        assert result["confidence"] > 0.5
        assert "A" in result["metadata"]["antigens"]
    
    def test_blood_type_o_validation(self):
        """Test O blood type validation"""
        agent = MedicalRulesAgent()
        result = agent.analyze({
            "cnn_prediction": "O",
            "agglutination_pattern": {}
        })
        
        assert result["prediction"] == "O"
        assert result["confidence"] > 0.5
        assert len(result["metadata"]["antigens"]) == 0
    
    def test_invalid_prediction(self):
        """Test handling of invalid blood type"""
        agent = MedicalRulesAgent()
        result = agent.analyze({
            "cnn_prediction": "INVALID",
            "agglutination_pattern": {}
        })
        
        assert result["prediction"] == "INCONCLUSIVE"
        assert result["confidence"] < 0.5

class TestConfidenceAssessmentAgent:
    """Test confidence assessment agent"""
    
    def test_initialization(self):
        """Test agent initialization"""
        agent = ConfidenceAssessmentAgent()
        assert agent.agent_id == "agent_004"
        assert agent.agent_name == "Confidence Assessment Agent"
    
    def test_high_confidence_assessment(self, sample_agent_outputs):
        """Test high confidence scenario"""
        agent = ConfidenceAssessmentAgent()
        result = agent.analyze({
            "agent_predictions": sample_agent_outputs,
            "image_quality": 0.95
        })
        
        assert result["prediction"] in ["HIGH", "MODERATE", "LOW", "VERY_LOW"]
        assert 0.0 <= result["confidence"] <= 1.0
        assert "agreement_ratio" in result["metadata"]
    
    def test_low_confidence_assessment(self, sample_agent_outputs):
        """Test low confidence scenario (conflicting predictions)"""
        conflicting_outputs = sample_agent_outputs.copy()
        conflicting_outputs[1]["prediction"] = "AB"  # Create disagreement
        
        agent = ConfidenceAssessmentAgent()
        result = agent.analyze({
            "agent_predictions": conflicting_outputs,
            "image_quality": 0.5
        })
        
        assert result["metadata"]["agreement_ratio"] < 1.0
        assert result["confidence"] < 0.85

class TestSafetyEthicsAgent:
    """Test safety and ethics agent"""
    
    def test_initialization(self):
        """Test agent initialization"""
        agent = SafetyEthicsAgent()
        assert agent.agent_id == "agent_005"
        assert agent.agent_name == "Safety & Ethics Agent"
        assert agent.confidence_threshold_for_deployment == 0.75
    
    def test_safe_deployment(self, sample_agent_outputs):
        """Test safe deployment scenario"""
        agent = SafetyEthicsAgent()
        result = agent.analyze({
            "agent_assessments": sample_agent_outputs,
            "combined_confidence": 0.88,
            "image_encrypted": True,
            "audit_logged": True
        })
        
        assert result["prediction"] == "SAFE_FOR_DEPLOYMENT"
        assert result["confidence"] > 0.7
        assert result["agree"] == True
    
    def test_unsafe_deployment(self, sample_agent_outputs):
        """Test unsafe deployment scenario"""
        agent = SafetyEthicsAgent()
        result = agent.analyze({
            "agent_assessments": sample_agent_outputs,
            "combined_confidence": 0.5,
            "image_encrypted": False,
            "audit_logged": False
        })
        
        assert result["prediction"] == "NEEDS_REVIEW"
        assert result["confidence"] < 0.7
        assert result["agree"] == False
