"""
Application configuration and MongoDB connection.
Use environment variable MONGODB_URI to override in production.
"""
import os
from urllib.parse import urlparse
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection

# MongoDB connection string (override with MONGODB_URI env var for production)
MONGODB_URI = os.getenv(
    "MONGODB_URI",
    "mongodb+srv://chongjayden0928_db_user:jayden_0928@firstround.memez4f.mongodb.net/?appName=FirstRound",
)

# Database name - change if you use a specific DB name
DB_NAME = os.getenv("MONGODB_DB_NAME", "FirstRound")

# Frontend origin for CORS (your frontend runs here)
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")

_client: MongoClient | None = None


def get_mongo_server_name() -> str:
    """Return the MongoDB server host from the URI (no credentials)."""
    parsed = urlparse(MONGODB_URI)
    return parsed.hostname or parsed.netloc or "unknown"


def get_mongo_client() -> MongoClient:
    """Get or create MongoDB client (singleton)."""
    global _client
    if _client is None:
        _client = MongoClient(MONGODB_URI)
    return _client


def get_database() -> Database:
    """Get the default database."""
    return get_mongo_client()[DB_NAME]


def get_collection(name: str) -> Collection:
    """Get a collection by name."""
    return get_database()[name]


def close_mongo_connection():
    """Close MongoDB connection (e.g. on app shutdown)."""
    global _client
    if _client is not None:
        _client.close()
        _client = None
