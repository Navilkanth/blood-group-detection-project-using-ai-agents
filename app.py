from flask import Flask, request, jsonify
from predict import predict_blood_group
import os
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))
from utils.model_manager import ModelManager

app = Flask(__name__)

# Verify model on startup
@app.before_request
def check_model():
    """Check model availability on first request"""
    if not hasattr(app, 'model_checked'):
        try:
            ModelManager.load_model()
            app.logger.info("✓ Model loaded successfully")
        except Exception as e:
            app.logger.error(f"✗ Failed to load model: {e}")
        app.model_checked = True

@app.route('/status', methods=['GET'])
def status():
    """Get application status including model availability"""
    status_info = ModelManager.get_status()
    return jsonify({
        'status': 'healthy',
        'model': {
            'available': status_info['model_found'],
            'path': status_info['model_path']
        },
        'labels': {
            'available': status_info['labels_found'],
            'path': status_info['labels_path'],
            'classes': status_info['labels']
        }
    })

@app.route('/predict', methods=['POST'])
def predict():
    """Predict blood group from uploaded image"""
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Save temporarily
    filepath = f"temp_{file.filename}"
    try:
        file.save(filepath)
        
        # Get prediction
        result = predict_blood_group(filepath)
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # Clean up
        if os.path.exists(filepath):
            os.remove(filepath)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
