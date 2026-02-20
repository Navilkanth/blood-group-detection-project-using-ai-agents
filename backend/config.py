import os
from dotenv import load_dotenv

# Load environment variables from both backend and root
load_dotenv()
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

class Config:
    """Base configuration"""
    DEBUG = False
    TESTING = False
    FLASK_ENV = "production"
    
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./blood_group.db")
    MONGODB_URI = os.getenv("MONGODB_URI", "mongodb+srv://admin:admin@cluster0.mongodb.net/?retryWrites=true&w=majority")
    MONGODB_DB = os.getenv("MONGODB_DB", "blood_group_analysis")
    
    # Upload settings
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "../uploads")
    MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "tiff"}
    
    # Model paths - Search for the trained model in common locations
    @staticmethod
    def get_model_path():
        filename = "blood_model_FIXED.keras"
        potential_paths = [
            r"C:\Users\navin\Downloads\blood_model_FIXED.keras",
            os.path.abspath(os.path.join(os.path.dirname(__file__), "..", filename)),
            os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", filename)),
            os.path.abspath(os.path.join(os.path.dirname(__file__), filename)),
        ]
        for p in potential_paths:
            if os.path.exists(p):
                return p
        return potential_paths[0] # Default

    @staticmethod
    def get_label_path():
        filename = "MODEL LABEL.json"
        potential_paths = [
            os.path.abspath(os.path.join(os.path.dirname(__file__), "models", filename)),
            r"C:\Users\navin\Downloads\MODEL LABEL.json",
        ]
        for p in potential_paths:
            if os.path.exists(p):
                return p
        return potential_paths[0]

    MODEL_PATHS = {
        "agglutination_cnn": get_model_path(),
        "labels": get_label_path(),
        "quality_model": None, # Optional
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
