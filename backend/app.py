from flask import Flask
from flask_cors import CORS
import os
import sys
import logging

# Support running as both module and script
try:
    from backend.config import config
    from backend.routes import prediction_routes, upload_routes, health_routes
    from backend.utils.logger import setup_logger
except ImportError:
    # Fallback for running directly: python app.py
    from config import config
    from routes import prediction_routes, upload_routes, health_routes
    from utils.logger import setup_logger

# Setup logging
app_logger = setup_logger(__name__, os.getenv("LOG_LEVEL", "INFO"))

def create_app(config_name="development"):
    """Application factory"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Setup application logger
    app.logger.handlers = app_logger.handlers
    app.logger.setLevel(app_logger.level)
    
    # Enable CORS
    CORS(app)
    
    # Create required directories
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    app.logger.info(f"Flask app created with config: {config_name}")
    app.logger.info(f"Using device: {'GPU (CUDA)' if app.config['CNN_SETTINGS']['use_gpu'] else 'CPU'}")
    
    # Initialize database
    from backend.utils.mongodb import init_db
    init_db()
    app.logger.info("MongoDB initialized")
    
    # Register blueprints
    app.register_blueprint(health_routes.bp)
    app.register_blueprint(upload_routes.bp)
    app.register_blueprint(prediction_routes.bp)
    
    # Verify Model Existence
    model_path = app.config["MODEL_PATHS"].get("agglutination_cnn")
    if model_path and os.path.exists(model_path):
        app.logger.info(f"✅ Verified: Trained model found at {model_path}")
    else:
        app.logger.error(f"❌ Alert: Trained model NOT found at {model_path}")

    app.logger.info("API routes registered")
    
    # Root endpoint
    @app.route("/")
    def root():
        """Root endpoint with API information"""
        return {
            "service": "Blood Group Classification API",
            "version": "1.0.0",
            "status": "running",
            "endpoints": {
                "health": "/api/health",
                "upload": "/api/upload",
                "predict": "/api/predict",
                "results": "/api/results/<prediction_id>"
            }
        }, 200
    
    # Error handlers
    @app.errorhandler(400)
    def bad_request(error):
        app.logger.warning(f"Bad request: {error}")
        return {"error": "Bad request"}, 400
    
    @app.errorhandler(404)
    def not_found(error):
        app.logger.warning(f"Not found: {error}")
        return {"error": "Resource not found"}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f"Internal error: {error}")
        # Return actual error message for debugging
        return {"error": "Internal server error", "message": str(error)}, 500
    
    return app

if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("🩸 BLOOD GROUP CLASSIFICATION - BACKEND SERVER")
    print("=" * 80)
    
    app = create_app(os.getenv("FLASK_ENV", "development"))
    
    config_name = os.getenv("FLASK_ENV", "development").upper()
    debug_mode = app.debug
    
    print(f"\n📍 Server: http://localhost:5000")
    print(f"📍 Config: {config_name}")
    print(f"📍 Debug: {debug_mode}")
    print(f"📍 Device: {'GPU (CUDA)' if app.config['CNN_SETTINGS']['use_gpu'] else 'CPU'}")
    
    print("\n" + "=" * 80)
    print("✅ READY - Backend is starting...")
    print("=" * 80 + "\n")
    
    try:
        app.run(host="0.0.0.0", port=5000, debug=debug_mode)
    except KeyboardInterrupt:
        print("\n\n✋ Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()