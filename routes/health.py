"""
Health and status routes - for frontend to verify backend and MongoDB connection.
"""
from flask import Blueprint, jsonify
from config.config import get_mongo_client

health_bp = Blueprint("health", __name__, url_prefix="/api")


@health_bp.route("/health", methods=["GET"])
def health():
    """Basic health check."""
    return jsonify({"status": "ok", "service": "FirstRound-Backend"})


@health_bp.route("/health/db", methods=["GET"])
def health_db():
    """Check MongoDB connection (so frontend can verify backend is connected to DB)."""
    try:
        client = get_mongo_client()
        client.admin.command("ping")
        return jsonify({"status": "ok", "mongodb": "connected"})
    except Exception as e:
        return jsonify({"status": "error", "mongodb": str(e)}), 503
