"""
Job Description model - defines the structure for job description documents in MongoDB.
Collection: jobDescriptions
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class JobDescription(BaseModel):
    """Job Description model matching the jobDescriptions collection."""
    job_title: str
    role_overview: str
    responsibilities: List[str]
    required_skills: List[str]
    preferred_skills: List[str] = []
    experience_level: str
    salary_range_display: str
    salary_range_min: float
    salary_range_max: float
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)


class JobDescriptionCreate(BaseModel):
    """Schema for creating a new job description."""
    job_title: str
    role_overview: str
    responsibilities: List[str]
    required_skills: List[str]
    preferred_skills: List[str] = []
    experience_level: str
    salary_range_display: str
    salary_range_min: float
    salary_range_max: float


class JobDescriptionResponse(BaseModel):
    """Schema for job description response."""
    id: str
    job_title: str
    role_overview: str
    responsibilities: List[str]
    required_skills: List[str]
    preferred_skills: List[str]
    experience_level: str
    salary_range_display: str
    salary_range_min: float
    salary_range_max: float
    created_at: datetime
    updated_at: datetime
