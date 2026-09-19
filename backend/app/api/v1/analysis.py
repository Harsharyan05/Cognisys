"""
Analysis API

Author: Harsh Aryan
Project: Cognisys
"""

from fastapi import APIRouter

from app.schemas.analysis import (
    AnalysisRequest,
    AnalysisResponse,
)

from app.services.analysis_service import AnalysisService

from app.services.repository_service import RepositoryService


router = APIRouter(
    prefix="/analysis",
    tags=["Analysis"],
)


@router.post(
    "/analyze",
    response_model=AnalysisResponse,
)
def analyze_repository(request: AnalysisRequest):

    clone = RepositoryService.clone_repository(
        str(request.repository_url)
    )

    result = AnalysisService.analyze(
        clone["local_path"]
    )

    return {
        "status": "success",
        **result,
    }