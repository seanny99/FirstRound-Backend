"""
Resume API - read from the resume MongoDB collection.
"""

from flask import Blueprint, current_app, jsonify

# Collection name (must match model.resume.COLLECTION_NAME)
RESUME_COLLECTION = "review"


def serialize_review(doc):
    """Convert a resume document for JSON (ObjectId and datetime to str)."""
    if not doc:
        return None
    out = dict(doc)
    if "_id" in out:
        out["_id"] = str(out["_id"])
    return out


reviews_bp = Blueprint("reviews", __name__, url_prefix="/api")


@reviews_bp.route("/reviews", methods=["GET"], strict_slashes=False)
def list_reviews():
    """Return all reviews from the review collection."""
    try:
        db = current_app.db
        coll = db[RESUME_COLLECTION]
        cursor = coll.find({}).sort("created_at", -1)
        reviews = [serialize_review(d) for d in cursor]
        return jsonify({"reviews": reviews, "count": len(reviews)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
