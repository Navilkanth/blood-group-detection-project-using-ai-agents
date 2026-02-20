"""
Flask API endpoint tests
"""
import pytest
import os
from io import BytesIO
from PIL import Image

class TestHealthEndpoint:
    """Test health check endpoint"""
    
    def test_health_check(self, client):
        """Test GET /api/health"""
        response = client.get("/api/health")
        
        assert response.status_code == 200
        data = response.get_json()
        assert data["status"] == "healthy"
        assert "service" in data
        assert "version" in data

class TestUploadEndpoint:
    """Test image upload endpoint"""
    
    def test_upload_valid_image(self, client, tmp_path):
        """Test POST /api/upload with valid image"""
        # Create test image
        image = Image.new('RGB', (224, 224), color='red')
        img_io = BytesIO()
        image.save(img_io, 'JPEG')
        img_io.seek(0)
        
        response = client.post(
            "/api/upload",
            data={"file": (img_io, "test_sample.jpg")},
            content_type="multipart/form-data"
        )
        
        assert response.status_code == 201
        data = response.get_json()
        assert "file_id" in data
        assert "filename" in data
        assert data["filename"].endswith(".jpg")
    
    def test_upload_no_file(self, client):
        """Test POST /api/upload without file"""
        response = client.post(
            "/api/upload",
            data={},
            content_type="multipart/form-data"
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data
    
    def test_upload_invalid_file_type(self, client):
        """Test POST /api/upload with invalid file type"""
        response = client.post(
            "/api/upload",
            data={"file": (BytesIO(b"test"), "test.txt")},
            content_type="multipart/form-data"
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data

class TestPredictionEndpoint:
    """Test prediction endpoint"""
    
    def test_predict_missing_file_id(self, client):
        """Test POST /api/predict without file_id"""
        response = client.post(
            "/api/predict",
            json={}
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data
    
    def test_predict_nonexistent_file(self, client):
        """Test POST /api/predict with nonexistent file"""
        response = client.post(
            "/api/predict",
            json={"file_id": "nonexistent_file_id"}
        )
        
        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data

class TestResultsEndpoint:
    """Test results retrieval endpoint"""
    
    def test_results_nonexistent_prediction(self, client):
        """Test GET /api/results with nonexistent prediction ID"""
        response = client.get("/api/results/nonexistent_id")
        
        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data
