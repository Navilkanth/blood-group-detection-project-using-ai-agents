"""
Backend Testing Script - Verify all endpoints are working
"""
import requests
import json
from time import sleep
from tensorflow.keras.models import load_model
from backend.config import Config

BASE_URL = "http://localhost:5000"

# Load the model
model_path = Config.MODEL_PATHS.get("agglutination_cnn")
model = load_model(model_path)

# Verify it loaded correctly
print(model.summary())

def test_endpoints():
    """Test all backend endpoints"""
    
    print("\n" + "=" * 80)
    print("🧪 BACKEND API TESTING")
    print("=" * 80 + "\n")
    
    # Test 1: Root endpoint
    print("1️⃣  Testing Root Endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ Root endpoint working")
            print(f"   Response: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Cannot connect to backend: {e}")
        print("   Make sure backend is running: python app.py")
        return
    
    # Test 2: Health check
    print("\n2️⃣  Testing Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        if response.status_code == 200:
            print("✅ Health check endpoint working")
            print(f"   Response: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")
    
    # Test 3: Upload endpoint (without file)
    print("\n3️⃣  Testing Upload Endpoint (expected to fail - no file)...")
    try:
        response = requests.post(f"{BASE_URL}/api/upload")
        if response.status_code == 400:
            print("✅ Upload endpoint is working (correctly rejected no file)")
            print(f"   Response: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"⚠️  Unexpected response: {response.status_code}")
    except Exception as e:
        print(f"❌ Upload endpoint error: {e}")
    
    # Test 4: Predict endpoint (without file_id)
    print("\n4️⃣  Testing Predict Endpoint (expected to fail - no file_id)...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/predict",
            json={}
        )
        if response.status_code == 400:
            print("✅ Predict endpoint is working (correctly rejected)")
            print(f"   Response: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"⚠️  Unexpected response: {response.status_code}")
    except Exception as e:
        print(f"❌ Predict endpoint error: {e}")
    
    print("\n" + "=" * 80)
    print("✨ All endpoints tested!")
    print("=" * 80 + "\n")
    
    print("📍 Next Steps:")
    print("   1. Upload a blood sample image:")
    print("      curl -X POST -F \"file=@image.jpg\" http://localhost:5000/api/upload")
    print("\n   2. Predict blood group:")
    print("      curl -X POST -H \"Content-Type: application/json\" \\")
    print("           -d '{\"file_id\":\"<file_id>\"}' \\")
    print("           http://localhost:5000/api/predict")
    print()

if __name__ == "__main__":
    test_endpoints()
