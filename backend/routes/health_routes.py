from flask import Blueprint, jsonify

bp = Blueprint("health", __name__, url_prefix="/api")

@bp.route("/health", methods=["GET"])
def health_check():
    """System health check"""
    return jsonify({
        "status": "healthy",
        "service": "Blood Group Classification API",
        "version": "1.0.0"
    }), 200
