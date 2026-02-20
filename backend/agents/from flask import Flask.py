from flask import Flask
from flask_cors import CORS
import os
import logging
from backend.config import config
from backend.routes import prediction_routes, upload_routes, health_routes
from backend.utils.logger import setup_logger

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
    from backend.utils.database import init_db
    init_db()
    
    # Register blueprints
    app.register_blueprint(health_routes.bp)
    app.register_blueprint(upload_routes.bp)
    app.register_blueprint(prediction_routes.bp)
    
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
        return {"error": "Internal server error"}, 500
    
    return app

if __name__ == "__main__":
    app = create_app(os.getenv("FLASK_ENV", "development"))
    app.run(host="0.0.0.0", port=5000, debug=app.debug)
