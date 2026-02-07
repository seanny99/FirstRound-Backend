"""
Resume API - read from the resume MongoDB collection.
"""
from flask import Blueprint, current_app, jsonify

# Collection name (must match model.resume.COLLECTION_NAME)
RESUME_COLLECTION = "resume"


def serialize_resume(doc):
    """Convert a resume document for JSON (ObjectId and datetime to str)."""
    if not doc:
        return None
    out = dict(doc)
    if "_id" in out:
        out["_id"] = str(out["_id"])
    for key in ("created_at", "updated_at"):
        if key in out and out[key] is not None:
            out[key] = out[key].isoformat()
    return out


resumes_bp = Blueprint("resumes", __name__, url_prefix="/api")


@resumes_bp.route("/resumes", methods=["GET"], strict_slashes=False)
def list_resumes():
    """Return all resumes from the resume collection."""
    try:
        db = current_app.db
        coll = db[RESUME_COLLECTION]
        cursor = coll.find({}).sort("created_at", -1)
        resumes = [serialize_resume(d) for d in cursor]
        return jsonify({"resumes": resumes, "count": len(resumes)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
