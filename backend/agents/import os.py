import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    DEBUG = False
    TESTING = False
    FLASK_ENV = "production"
    
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./blood_group.db")
    
    # Upload settings
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "../uploads")
    MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "tiff"}
    
    # Model paths - UPDATE THESE WITH YOUR ACTUAL MODEL PATHS
    MODEL_PATHS = {
        "agglutination_cnn": os.getenv(
            "AGGLUTINATION_MODEL_PATH",
            os.path.join(os.path.dirname(__file__), "models/agglutination_model.pth")
        ),
        "quality_model": os.getenv(
            "QUALITY_MODEL_PATH",
            os.path.join(os.path.dirname(__file__), "models/quality_model.pth")
        ),
    }
    
    # CNN Inference settings
    CNN_SETTINGS = {
        "batch_size": 1,
        "use_gpu": os.getenv("USE_GPU", "true").lower() == "true",
        "confidence_threshold": float(os.getenv("CNN_CONFIDENCE_THRESHOLD", "0.5")),
        "enable_caching": True,
    }
    
    # Agent settings
    CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", "0.7"))
    AGENT_COUNT = 5
    CONSENSUS_THRESHOLD = float(os.getenv("CONSENSUS_THRESHOLD", "0.6"))
    
    # Medical compliance
    HIPAA_LOGGING = os.getenv("HIPAA_LOGGING", "true").lower() == "true"
    ENCRYPT_IMAGES = os.getenv("ENCRYPT_IMAGES", "true").lower() == "true"
    KEEP_PREDICTION_HISTORY = True
    AUDIT_LOG_RETENTION_DAYS = 2555  # ~7 years
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    FLASK_ENV = "development"
    LOG_LEVEL = "DEBUG"

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DATABASE_URL = "sqlite:///:memory:"
    LOG_LEVEL = "DEBUG"

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    FLASK_ENV = "production"
    LOG_LEVEL = "WARNING"

config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
