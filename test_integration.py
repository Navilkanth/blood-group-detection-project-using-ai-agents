"""
Integration Test Utility
Tests model loading, label loading, and prediction pipeline
"""

import sys
import os
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

def test_model_manager():
    """Test the centralized model manager"""
    print("\n" + "="*70)
    print("TESTING CENTRALIZED MODEL MANAGER")
    print("="*70)
    
    from utils.model_manager import ModelManager
    
    # Test 1: Get model path
    print("\n[Test 1] Getting model path...")
    try:
        model_path = ModelManager.get_model_path()
        print(f"✅ Model path: {model_path}")
        print(f"   File exists: {os.path.exists(model_path)}")
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Test 2: Get labels path
    print("\n[Test 2] Getting labels path...")
    try:
        labels_path = ModelManager.get_labels_path()
        print(f"✅ Labels path: {labels_path}")
        if labels_path:
            print(f"   File exists: {os.path.exists(labels_path)}")
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Test 3: Load labels
    print("\n[Test 3] Loading blood group labels...")
    try:
        labels = ModelManager.load_labels()
        print(f"✅ Loaded {len(labels)} blood group classes: {labels}")
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Test 4: Get status
    print("\n[Test 4] Getting model status...")
    try:
        status = ModelManager.get_status()
        print(f"✅ Model available: {status['model_found']}")
        print(f"✅ Labels available: {status['labels_found']}")
        print(f"✅ Blood groups: {status['labels']}")
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Test 5: Load model
    print("\n[Test 5] Loading TensorFlow/Keras model...")
    try:
        model = ModelManager.load_model()
        print(f"✅ Model loaded successfully!")
        print(f"   Input shape: {model.input_shape}")
        print(f"   Output shape: {model.output_shape}")
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    print("\n" + "="*70)
    print("✅ ALL MODEL MANAGER TESTS PASSED!")
    print("="*70)
    return True

def test_predict_import():
    """Test predict module imports"""
    print("\n" + "="*70)
    print("TESTING PREDICT MODULE")
    print("="*70)
    
    print("\n[Test 1] Importing predict module...")
    try:
        from predict import predict_blood_group
        print("✅ predict_blood_group imported successfully")
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    print("\n[Test 2] Checking function signature...")
    try:
        import inspect
        sig = inspect.signature(predict_blood_group)
        print(f"✅ Function signature: {sig}")
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    print("\n" + "="*70)
    print("✅ ALL PREDICT MODULE TESTS PASSED!")
    print("="*70)
    return True

def test_app_integration():
    """Test Flask app integration"""
    print("\n" + "="*70)
    print("TESTING FLASK APP INTEGRATION")
    print("="*70)
    
    print("\n[Test 1] Importing Flask app...")
    try:
        from app import app
        print("✅ Flask app imported successfully")
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    print("\n[Test 2] Checking app routes...")
    try:
        routes = [rule.rule for rule in app.url_map.iter_rules()]
        print(f"✅ Registered routes: {routes}")
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    print("\n[Test 3] Testing /status endpoint...")
    try:
        with app.test_client() as client:
            response = client.get('/status')
            print(f"✅ Response status: {response.status_code}")
            if response.status_code == 200:
                data = response.get_json()
                print(f"   Model available: {data['model']['available']}")
                print(f"   Blood groups: {data['labels']['classes']}")
            else:
                print(f"❌ Unexpected status code: {response.status_code}")
                return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    print("\n[Test 4] Testing /health endpoint...")
    try:
        with app.test_client() as client:
            response = client.get('/health')
            print(f"✅ Response status: {response.status_code}")
            print(f"   Response: {response.get_json()}")
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    print("\n" + "="*70)
    print("✅ ALL APP INTEGRATION TESTS PASSED!")
    print("="*70)
    return True

def main():
    """Run all tests"""
    print("\n" + "#"*70)
    print("# BLOOD GROUP CLASSIFICATION PROJECT - INTEGRATION TESTS")
    print("#"*70)
    print(f"Python: {sys.version}")
    print(f"Working Directory: {os.getcwd()}")
    
    all_passed = True
    
    # Run tests
    if not test_model_manager():
        all_passed = False
    
    if not test_predict_import():
        all_passed = False
    
    if not test_app_integration():
        all_passed = False
    
    # Summary
    print("\n" + "#"*70)
    if all_passed:
        print("# ✅ ALL TESTS PASSED! Project is ready to use.")
    else:
        print("# ❌ SOME TESTS FAILED! Please review errors above.")
    print("#"*70 + "\n")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
