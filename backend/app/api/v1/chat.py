
"""
Repository-specific Chat API for Cognisys.
"""

from threading import RLock
from fastapi import APIRouter, HTTPException

from app.repository.repository_manager import RepositoryManager
from app.ai.repository_indexer import RepositoryIndexer
from app.ai.rag_pipeline import RAGPipeline
from app.services.repository_service import RepositoryService
from app.schemas.chat import ChatRequest, ChatResponse


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)

# Initial in-memory session store.
# Each entry contains the repository URL and its RAG pipeline.
_chat_sessions = {}
_sessions_lock = RLock()


@router.post("", response_model=ChatResponse)
def chat(request: ChatRequest):
    question = request.question.strip()
    repository_url = str(request.repository_url).rstrip("/")

    if not question:
        raise HTTPException(
            status_code=422,
            detail="Question cannot be empty.",
        )

    session_id = request.session_id.strip()

    if not session_id:
        raise HTTPException(
            status_code=422,
            detail="Session ID cannot be empty.",
        )

    try:
        with _sessions_lock:
            session = _chat_sessions.get(session_id)

            if session is not None:
                if session["repository_url"] != repository_url:
                    raise HTTPException(
                        status_code=409,
                        detail=(
                            "This session is already associated "
                            "with a different repository. "
                            "Use a new session_id."
                        ),
                    )

                rag_pipeline = session["pipeline"]

            else:
                # Clone repository.
                clone = RepositoryService.clone_repository(
                    repository_url
                )
                repository_path = clone["local_path"]

                # Register repository.
                repository_manager = RepositoryManager()

                repository_manager.register_repository(
                    repository_url=repository_url,
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

                # Index repository code.
                indexer = RepositoryIndexer(repository_path)
                index_result = indexer.index()

                repository_manager.mark_indexed(
                    repository_id,
                    commit_sha=clone.get("commit_sha"),
                )

                # Create pipeline with session conversation memory.
                rag_pipeline = RAGPipeline(
                    vector_store_directory=index_result["vector_store"],
                    repository_path=repository_path,
                )

                _chat_sessions[session_id] = {
                    "repository_url": repository_url,
                    "pipeline": rag_pipeline,
                }

        # Ask using the existing RAG pipeline.
        result = rag_pipeline.ask(question)

        return ChatResponse(
            status="success",
            session_id=session_id,
            question=question,
            answer=result.get("answer", ""),
            citations=result.get("citations", []),
            conversation_size=result.get(
                "conversation_size", 0
            ),
        )

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Chat request failed: {str(exc)}",
        ) from exc
