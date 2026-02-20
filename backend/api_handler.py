from backend.model_loader import BloodGroupClassifier
import json

class BloodGroupAPI:
    def __init__(self, model_path):
        self.classifier = BloodGroupClassifier(model_path)
    
    def classify_from_file(self, image_path):
        """API endpoint for file-based classification"""
        try:
            result = self.classifier.predict(image_path)
            return {
                'status': 'success',
                'data': result
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def classify_from_url(self, image_url):
        """API endpoint for URL-based classification"""
        try:
            import urllib.request
            import tempfile
            
            # Download image
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp:
                urllib.request.urlretrieve(image_url, tmp.name)
                result = self.classifier.predict(tmp.name)
            
            return {
                'status': 'success',
                'data': result
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }


# Usage in your backend
if __name__ == "__main__":
    # Use configured model path when running locally
    try:
        from backend.config import Config
        model_path = Config.MODEL_PATHS.get("agglutination_cnn")
    except Exception:
        model_path = r"C:\Users\navin\Downloads\blood_model_FIXED.keras"

    api = BloodGroupAPI(model_path)
    
    # Test
    # result = api.classify_from_file("test_image.jpg")
    # print(json.dumps(result, indent=2))
