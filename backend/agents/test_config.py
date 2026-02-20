"""
Configuration tests
"""
import pytest
from backend.config import config, DevelopmentConfig, TestingConfig, ProductionConfig

class TestConfiguration:
    """Test configuration management"""
    
    def test_development_config(self):
        """Test development configuration"""
        cfg = DevelopmentConfig()
        assert cfg.DEBUG == True
        assert cfg.FLASK_ENV == "development"
    
    def test_testing_config(self):
        """Test testing configuration"""
        cfg = TestingConfig()
        assert cfg.TESTING == True
        assert "memory" in cfg.DATABASE_URL
    
    def test_production_config(self):
        """Test production configuration"""
        cfg = ProductionConfig()
        assert cfg.DEBUG == False
        assert cfg.FLASK_ENV == "production"
    
    def test_config_values(self):
        """Test configuration values are set"""
        cfg = DevelopmentConfig()
        assert cfg.CONFIDENCE_THRESHOLD > 0
        assert cfg.AGENT_COUNT == 5
        assert cfg.CONSENSUS_THRESHOLD > 0
    
    def test_model_paths_exist(self):
        """Test model paths configuration"""
        cfg = DevelopmentConfig()
        assert "agglutination_cnn" in cfg.MODEL_PATHS
        assert "quality_model" in cfg.MODEL_PATHS
