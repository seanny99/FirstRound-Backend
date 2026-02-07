"""
Job Description service - business logic for job description operations.
"""
from datetime import datetime
from typing import List, Optional
from bson import ObjectId
from pymongo.collection import Collection

from config.config import get_collection
from model.jobDescription import JobDescription, JobDescriptionCreate, JobDescriptionResponse


class JobDescriptionService:
    """Service class for job description CRUD operations."""
    
    def __init__(self):
        self.collection: Collection = get_collection("jobDescriptions")
    
    def createJobDescription(self, jobData: JobDescriptionCreate) -> JobDescriptionResponse:
        """
        Create a new job description in MongoDB.
        
        Args:
            jobData: Job description data from the request
            
        Returns:
            Created job description with ID
        """
        # Convert Pydantic model to dict
        jobDict = jobData.dict()
        
        # Add metadata
        jobDict["created_at"] = datetime.utcnow()
        jobDict["updated_at"] = datetime.utcnow()
        
        # Insert into MongoDB
        result = self.collection.insert_one(jobDict)
        
        # Retrieve the created document
        createdJob = self.collection.find_one({"_id": result.inserted_id})
        
        # Convert to response model
        return self._documentToResponse(createdJob)
    
    def getAllJobDescriptions(self) -> List[JobDescriptionResponse]:
        """
        Get all job descriptions.
        
        Returns:
            List of job descriptions
        """
        # Fetch from MongoDB, sorted by creation date (newest first)
        cursor = self.collection.find({}).sort("created_at", -1)
        
        # Convert to response models
        return [self._documentToResponse(doc) for doc in cursor]
    
    def getJobDescriptionById(self, jobId: str) -> Optional[JobDescriptionResponse]:
        """
        Get a single job description by ID.
        
        Args:
            jobId: MongoDB ObjectId as string
            
        Returns:
            Job description or None if not found
        """
        try:
            doc = self.collection.find_one({"_id": ObjectId(jobId)})
            if doc:
                return self._documentToResponse(doc)
            return None
        except Exception:
            return None
    
    def updateJobDescription(
        self, 
        jobId: str, 
        jobData: JobDescriptionCreate
    ) -> Optional[JobDescriptionResponse]:
        """
        Update an existing job description.
        
        Args:
            jobId: MongoDB ObjectId as string
            jobData: Updated job description data
            
        Returns:
            Updated job description or None if not found
        """
        try:
            jobDict = jobData.dict()
            jobDict["updated_at"] = datetime.utcnow()
            
            result = self.collection.find_one_and_update(
                {"_id": ObjectId(jobId)},
                {"$set": jobDict},
                return_document=True
            )
            
            if result:
                return self._documentToResponse(result)
            return None
        except Exception:
            return None
    
    def deleteJobDescription(self, jobId: str) -> bool:
        """
        Delete a job description.
        
        Args:
            jobId: MongoDB ObjectId as string
            
        Returns:
            True if deleted, False otherwise
        """
        try:
            result = self.collection.delete_one({"_id": ObjectId(jobId)})
            return result.deleted_count > 0
        except Exception:
            return False
    
    def _documentToResponse(self, doc: dict) -> JobDescriptionResponse:
        """
        Convert MongoDB document to JobDescriptionResponse.
        
        Args:
            doc: MongoDB document
            
        Returns:
            JobDescriptionResponse model
        """
        doc["id"] = str(doc.pop("_id"))
        return JobDescriptionResponse(**doc)


# Singleton instance
jobDescriptionService = JobDescriptionService()
