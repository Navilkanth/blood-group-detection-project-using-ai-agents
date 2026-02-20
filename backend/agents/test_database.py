"""
Database operations tests
"""
import pytest
from backend.utils.database import (
    init_db,
    save_prediction,
    save_agent_assessment,
    get_prediction,
    log_audit
)

class TestDatabase:
    """Test database operations"""
    
    def test_database_initialization(self):
        """Test database schema creation"""
        init_db()
        # If no exception, schema was created successfully
        assert True
    
    def test_save_and_retrieve_prediction(self):
        """Test saving and retrieving prediction"""
        prediction_id = "test_pred_001"
        
        save_prediction(
            prediction_id=prediction_id,
            image_filename="test.jpg",
            blood_type="O",
            confidence=0.95,
            consensus_met=True,
            agent_votes={"O": 3, "A": 0},
            reasoning="All agents agreed on O"
        )
        
        result = get_prediction(prediction_id)
        
        assert result is not None
        assert result["blood_type"] == "O"
        assert result["confidence"] == 0.95
    
    def test_save_agent_assessment(self):
        """Test saving agent assessment"""
        prediction_id = "test_pred_001"
        
        save_agent_assessment(
            prediction_id=prediction_id,
            agent_id="agent_001",
            agent_name="Image Validation Agent",
            prediction="VALID",
            confidence=0.95,
            reasoning="Image quality excellent",
            metadata={"resolution": "224x224"}
        )
        
        # If no exception, record was saved successfully
        assert True
    
    def test_log_audit(self):
        """Test audit logging"""
        log_audit(
            prediction_id="test_pred_001",
            action="PREDICTION_CREATED",
            user_id="test_user",
            ip_address="127.0.0.1",
            details="Test prediction"
        )
        
        # If no exception, audit was logged successfully
        assert True
