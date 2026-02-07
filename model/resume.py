"""
Schema and constants for the resume MongoDB collection.
Stores candidate resume data. No DB reference to jobDescriptions; use target_role (string) to align with job titles.
"""
from datetime import datetime
from typing import Any

# Collection name
COLLECTION_NAME = "resume"


def experience_item(
    job_title: str,
    company: str,
    start_date: str,
    end_date: str,
    description_bullets: list[str],
) -> dict[str, Any]:
    """One work experience entry."""
    return {
        "job_title": job_title,
        "company": company,
        "start_date": start_date,
        "end_date": end_date,
        "description_bullets": description_bullets,
    }


def education_item(
    institution: str,
    degree: str,
    field: str | None = None,
    year: str | None = None,
) -> dict[str, Any]:
    """One education entry."""
    return {
        "institution": institution,
        "degree": degree,
        "field": field,
        "year": year,
    }


def resume_doc(
    full_name: str,
    email: str,
    phone: str,
    summary: str,
    experience: list[dict[str, Any]],
    education: list[dict[str, Any]],
    skills: list[str],
    target_role: str,
    created_at: datetime | None = None,
    updated_at: datetime | None = None,
) -> dict[str, Any]:
    """Build a document matching the resume schema."""
    now = datetime.utcnow()
    return {
        "full_name": full_name,
        "email": email,
        "phone": phone,
        "summary": summary,
        "experience": experience,
        "education": education,
        "skills": skills,
        "target_role": target_role,
        "created_at": created_at or now,
        "updated_at": updated_at or now,
    }


# ---------------------------------------------------------------------------
# Schema reference
# ---------------------------------------------------------------------------
# resume collection:
#
#   _id                 ObjectId
#   full_name           str
#   email               str
#   phone               str
#   summary             str     Short professional summary
#   experience          [       Work history
#     { job_title, company, start_date, end_date, description_bullets }
#   ]
#   education           [       Education history
#     { institution, degree, field?, year? }
#   ]
#   skills              [str]
#   target_role         str     Job title applying for (no DB ref to jobDescriptions)
#   created_at          datetime
#   updated_at          datetime
