"""
FirstRound Backend - main server startup.
Serves API for frontend at http://localhost:3000 with CORS enabled.
"""
import os
from flask import Flask
from flask_cors import CORS

from config.config import FRONTEND_ORIGIN, get_database, get_mongo_client, get_mongo_server_name

# Import route blueprints
from routes.health import health_bp


def create_app() -> Flask:
    app = Flask(__name__)

    # CORS: allow frontend at localhost:3000 to call this backend
    CORS(
        app,
        origins=[FRONTEND_ORIGIN, "http://127.0.0.1:3000"],
        allow_headers=["Content-Type", "Authorization"],
        supports_credentials=True,
    )

    # Register blueprints
    app.register_blueprint(health_bp)

    # Optional: expose DB on app for routes that need it
    @app.before_request
    def set_db():
        app.db = get_database()

    return app


app = create_app()


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    # Check MongoDB connection and print status
    server_name = get_mongo_server_name()
    print(f"[MongoDB] Server: {server_name}")
    try:
        get_mongo_client().admin.command("ping")
        print("[MongoDB] Connected successfully.")
    except Exception as e:
        print(f"[MongoDB] Not connected: {e}")
    # Run so frontend (localhost:3000) can call this backend (e.g. localhost:5000)
    app.run(host="0.0.0.0", port=port, debug=True)
