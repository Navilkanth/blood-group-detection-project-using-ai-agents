import pytest
import sys
import os
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

# Set working directory
os.chdir(str(backend_path))

@pytest.fixture
def app():
    """Create Flask app for testing"""
    os.environ["FLASK_ENV"] = "testing"
    from app import create_app
    app = create_app("testing")
    
    with app.app_context():
        yield app

@pytest.fixture
def client(app):
    """Flask test client"""
    return app.test_client()

@pytest.fixture
def test_image_path(tmp_path):
    """Create a test image"""
    import cv2
    import numpy as np
    
    # Create synthetic blood sample image
    image = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
    
    # Add some red tones (blood-like)
    image[:, :, 2] += 50  # Increase red channel
    
    image_path = tmp_path / "test_sample.jpg"
    cv2.imwrite(str(image_path), image)
    
    return str(image_path)

@pytest.fixture
def sample_agent_outputs():
    """Sample agent outputs for testing"""
    return [
        {
            "agent_id": "agent_001",
            "agent_name": "Image Validation Agent",
            "prediction": "VALID",
            "confidence": 0.95,
            "reasoning": "Image quality is excellent",
            "agree": True,
        },
        {
            "agent_id": "agent_002",
            "agent_name": "Agglutination Detection Agent",
            "prediction": "O",
            "confidence": 0.85,
            "reasoning": "No agglutination detected",
            "agree": True,
        },
        {
            "agent_id": "agent_003",
            "agent_name": "Medical Rules Agent",
            "prediction": "O",
            "confidence": 0.88,
            "reasoning": "Valid O blood type",
            "agree": True,
        },
    ]
