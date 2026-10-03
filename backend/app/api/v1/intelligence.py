"""
Intelligence API

Author: Harsh Aryan
Project: Cognisys
"""

from fastapi import APIRouter, HTTPException

from app.repository.repository_manager import RepositoryManager

from app.ai.repository_indexer import RepositoryIndexer
from app.ai.rag_pipeline import RAGPipeline

from app.architecture.architecture_engine import ArchitectureEngine

from app.impact.impact_engine import ImpactEngine

from app.graph.code_graph_engine import CodeGraphEngine
from app.graph.graph_query import GraphQuery
from app.graph.graph_aware_query import GraphAwareQuery

from app.intelligence.intelligence_engine import IntelligenceEngine

from app.schemas.intelligence import (
    IntelligenceAskRequest,
    IntelligenceAskResponse,
)

from app.services.repository_service import RepositoryService


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
    """
    Ask an intelligent question about a GitHub repository.

    Pipeline:

    GitHub Repository
        ↓
    Repository Clone
        ↓
    Repository Registration
        ↓
    Mark Indexing
        ↓
    Repository Indexing
        ↓
    RAG Pipeline
        ↓
    Architecture Analysis
        ↓
    Impact Analysis
        ↓
    Code Graph
        ↓
    Graph Query
        ↓
    Intelligence Engine
        ↓
    Unified Intelligence Response
    """

    # ---------------------------------------------------------
    # Validate request
    # ---------------------------------------------------------

    if not request.question.strip():
        raise HTTPException(
            status_code=422,
            detail="Question cannot be empty.",
        )

    # ---------------------------------------------------------
    # Clone repository
    # ---------------------------------------------------------

    clone = RepositoryService.clone_repository(
        str(request.repository_url)
    )

    repository_path = clone["local_path"]

    # ---------------------------------------------------------
    # Repository persistence
    # ---------------------------------------------------------

    repository_manager = RepositoryManager()

    repository_manager.register_repository(
        repository_url=str(request.repository_url),
        repository_name=clone["repository_name"],
        owner=clone.get("owner", ""),
        local_path=repository_path,
        commit_sha=clone.get("commit_sha"),
    )

    repository_id = (
        f"{clone.get('owner', '')}/"
        f"{clone['repository_name']}"
    )

    repository_manager.mark_indexing(
        repository_id
    )

    # ---------------------------------------------------------
    # Repository indexing
    # ---------------------------------------------------------

    indexer = RepositoryIndexer(
        repository_path
    )

    index_result = indexer.index()
    
    repository_manager.mark_indexed(
        repository_id,
        commit_sha=clone.get("commit_sha"),
    )

    # ---------------------------------------------------------
    # RAG pipeline
    # ---------------------------------------------------------

    rag_pipeline = RAGPipeline(
        vector_store_directory=index_result["vector_store"],
        repository_path=repository_path,
    )

    # ---------------------------------------------------------
    # Architecture intelligence
    # ---------------------------------------------------------

    architecture_engine = ArchitectureEngine(
        repository_path
    )

    # ---------------------------------------------------------
    # Impact intelligence
    # ---------------------------------------------------------

    impact_engine = ImpactEngine(
        architecture_engine
    )

    # ---------------------------------------------------------
    # Code graph intelligence
    # ---------------------------------------------------------

    code_graph_engine = CodeGraphEngine(
        repository_path
    )

    graph = code_graph_engine.build()

    graph_query = GraphQuery(
        graph
    )

    graph_aware_query = GraphAwareQuery(
        graph_query
    )

    # ---------------------------------------------------------
    # Intelligence engine
    # ---------------------------------------------------------

    intelligence_engine = IntelligenceEngine(
        rag_pipeline=rag_pipeline,
        architecture_engine=architecture_engine,
        impact_engine=impact_engine,
        code_graph_engine=code_graph_engine,
        graph_aware_query=graph_aware_query,
    )

    # ---------------------------------------------------------
    # Ask question
    # ---------------------------------------------------------

    result = intelligence_engine.ask(
        request.question
    )

    # ---------------------------------------------------------
    # Response
    # ---------------------------------------------------------

    return {
        "status": "success",
        **result,
    }