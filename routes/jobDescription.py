"""
Job Description routes - API endpoints for job description management.
"""
from flask import Blueprint, jsonify, request
from model.jobDescription import JobDescriptionCreate
from service.jobDescriptionService import jobDescriptionService

jobDescriptionBp = Blueprint("jobDescription", __name__, url_prefix="/api/jobDescriptions")


@jobDescriptionBp.route("", methods=["GET"])
def getJobDescriptions():
    """
    Get all job descriptions.
    """
    try:
        jobDescriptions = jobDescriptionService.getAllJobDescriptions()
        
        return jsonify({
            "status": "success",
            "count": len(jobDescriptions),
            "data": [job.dict() for job in jobDescriptions]
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@jobDescriptionBp.route("/<jobId>", methods=["GET"])
def getJobDescription(jobId: str):
    """Get a single job description by ID."""
    try:
        jobDescription = jobDescriptionService.getJobDescriptionById(jobId)
        
        if not jobDescription:
            return jsonify({
                "status": "error",
                "message": "Job description not found"
            }), 404
        
        return jsonify({
            "status": "success",
            "data": jobDescription.dict()
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@jobDescriptionBp.route("", methods=["POST"])
def createJobDescription():
    """
    Create a new job description.
    Request body should match JobDescriptionCreate schema.
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "status": "error",
                "message": "No data provided"
            }), 400
        
        # Validate and create job description
        jobData = JobDescriptionCreate(**data)
        createdJob = jobDescriptionService.createJobDescription(jobData)
        
        return jsonify({
            "status": "success",
            "message": "Job description created successfully",
            "data": createdJob.dict()
        }), 201
    except ValueError as e:
        return jsonify({
            "status": "error",
            "message": f"Validation error: {str(e)}"
        }), 400
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@jobDescriptionBp.route("/<jobId>", methods=["PUT"])
def updateJobDescription(jobId: str):
    """Update an existing job description."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "status": "error",
                "message": "No data provided"
            }), 400
        
        jobData = JobDescriptionCreate(**data)
        updatedJob = jobDescriptionService.updateJobDescription(jobId, jobData)
        
        if not updatedJob:
            return jsonify({
                "status": "error",
                "message": "Job description not found"
            }), 404
        
        return jsonify({
            "status": "success",
            "message": "Job description updated successfully",
            "data": updatedJob.dict()
        }), 200
    except ValueError as e:
        return jsonify({
            "status": "error",
            "message": f"Validation error: {str(e)}"
        }), 400
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@jobDescriptionBp.route("/<jobId>", methods=["DELETE"])
def deleteJobDescription(jobId: str):
    """Delete a job description."""
    try:
        success = jobDescriptionService.deleteJobDescription(jobId)
        
        if not success:
            return jsonify({
                "status": "error",
                "message": "Job description not found"
            }), 404
        
        return jsonify({
            "status": "success",
            "message": "Job description deleted successfully"
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
