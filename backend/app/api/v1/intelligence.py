"""
Intelligence API

Author: Harsh Aryan
Project: Cognisys
"""

from fastapi import APIRouter

from app.schemas.intelligence import (
    IntelligenceAskRequest,
    IntelligenceAskResponse,
)

from app.services.repository_service import RepositoryService

from app.ai.rag_pipeline import RAGPipeline

from app.architecture.architecture_engine import ArchitectureEngine

from app.impact.impact_engine import ImpactEngine

from app.intelligence.intelligence_engine import IntelligenceEngine


router = APIRouter(
    prefix="/intelligence",
    tags=["Intelligence"],
)


@router.post(
    "/ask",
    response_model=IntelligenceAskResponse,
)
def ask_intelligence(
    request: IntelligenceAskRequest,
):

    if not request.question.strip():
        from fastapi import HTTPException

        raise HTTPException(
            status_code=422,
            detail="Question cannot be empty.",
        )

    clone = RepositoryService.clone_repository(
        str(request.repository_url)
    )

    repository_path = clone["local_path"]

    rag_pipeline = RAGPipeline()

    architecture_engine = ArchitectureEngine(
        repository_path
    )

    impact_engine = ImpactEngine(
        architecture_engine
    )

    intelligence_engine = IntelligenceEngine(
        rag_pipeline=rag_pipeline,
        architecture_engine=architecture_engine,
        impact_engine=impact_engine,
    )

    result = intelligence_engine.ask(
        request.question
    )

    return {
        "status": "success",
        **result,
    }
