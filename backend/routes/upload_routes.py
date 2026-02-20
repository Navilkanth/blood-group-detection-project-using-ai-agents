from flask import Blueprint, request, jsonify, current_app
import os
from werkzeug.utils import secure_filename
import uuid
from datetime import datetime

bp = Blueprint("upload", __name__, url_prefix="/api")

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "tiff"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route("/upload", methods=["POST"])
def upload_image():
    """Upload blood sample image"""
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files["file"]
        
        if file.filename == "":
            return jsonify({"error": "No file selected"}), 400
        
        if not allowed_file(file.filename):
            return jsonify({"error": "Invalid file type"}), 400
        
        # Check file size (safely)
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0) # Reset pointer
        
        if file_size > current_app.config.get("MAX_UPLOAD_SIZE", 10 * 1024 * 1024):
            return jsonify({"error": "File too large"}), 413
        
        # Generate unique filename
        file_id = str(uuid.uuid4())
        ext = file.filename.rsplit(".", 1)[1].lower()
        filename = f"{file_id}.{ext}"
        
        # Save file
        filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)
        
        return jsonify({
            "file_id": file_id,
            "filename": filename,
            "upload_time": datetime.now().isoformat(),
            "message": "File uploaded successfully"
        }), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
