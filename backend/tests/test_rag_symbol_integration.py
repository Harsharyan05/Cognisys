"""
Tests for RAG Pipeline symbol-level retrieval integration.

Author: Harsh Aryan
Project: Cognisys
"""

from pathlib import Path

from app.ai.rag_pipeline import RAGPipeline
from app.ai.hybrid_retriever import HybridRetriever


def create_repository(repository_path):
    repository_path.mkdir()

    (repository_path / "auth.py").write_text(
        """class AuthService:

    def authenticate(self, username, password):
        return username == "admin"

    def logout(self):
        return True


def validate_token(token):
    return bool(token)
""",
        encoding="utf-8",
    )


# =========================================================
# RAG Pipeline Vector Store
# =========================================================


def test_rag_pipeline_accepts_repository_vector_store(
    tmp_path,
):

    vector_store = (
        tmp_path / "vector_db"
    )

    pipeline = RAGPipeline(
        vector_store_directory=str(
            vector_store
        )
    )

    assert (
        pipeline.hybrid_retriever
        .semantic_search
        .vector_store
        .output_directory
        == Path(vector_store)
    )


# =========================================================
# Symbol Search Integration
# =========================================================


def test_rag_pipeline_can_use_repository_specific_symbol_search(
    tmp_path,
):

    repository = (
        tmp_path / "sample_repo"
    )

    create_repository(repository)

    pipeline = RAGPipeline(
        vector_store_directory=str(
            tmp_path / "vector_db"
        )
    )

    from app.ai.symbol_semantic_search import (
        SymbolSemanticSearch,
    )

    pipeline.hybrid_retriever.repository_path = (
        repository
    )

    pipeline.hybrid_retriever.symbol_search = (
        SymbolSemanticSearch(
            repository_path=repository
        )
    )

    results = (
        pipeline.hybrid_retriever.retrieve(
            "authenticate user",
            top_k=5,
        )
    )

    assert results


# =========================================================
# Symbol Metadata
# =========================================================


def test_rag_pipeline_retrieval_contains_symbol_metadata(
    tmp_path,
):

    repository = (
        tmp_path / "sample_repo"
    )

    create_repository(repository)

    pipeline = RAGPipeline(
        vector_store_directory=str(
            tmp_path / "vector_db"
        )
    )

    from app.ai.symbol_semantic_search import (
        SymbolSemanticSearch,
    )

    pipeline.hybrid_retriever.repository_path = (
        repository
    )

    pipeline.hybrid_retriever.symbol_search = (
        SymbolSemanticSearch(
            repository_path=repository
        )
    )

    results = (
        pipeline.hybrid_retriever.retrieve(
            "authenticate user",
            top_k=5,
        )
    )

    assert results

    symbol_results = [
        embedding
        for score, embedding, distance in results
        if embedding.metadata.get(
            "symbol_id"
        )
    ]

    assert symbol_results

    embedding = symbol_results[0]

    assert (
        embedding.metadata["symbol_name"]
        == "authenticate"
    )

    assert (
        embedding.metadata["symbol_type"]
        == "method"
    )

    assert (
        embedding.metadata["parent_class"]
        == "AuthService"
    )


# =========================================================
# File + Symbol Retrieval
# =========================================================


def test_rag_pipeline_preserves_file_level_retrieval(
    tmp_path,
):

    repository = (
        tmp_path / "sample_repo"
    )

    create_repository(repository)

    vector_store_directory = (
        tmp_path / "vector_db"
    )

    # -----------------------------------------------------
    # Build repository-specific file-level vector index
    # -----------------------------------------------------

    from app.ai.repository_indexer import (
        RepositoryIndexer,
    )

    indexer = RepositoryIndexer(
        repository_path=repository
    )

    index_result = indexer.index()

    # -----------------------------------------------------
    # Create RAG pipeline using the generated vector store
    # -----------------------------------------------------

    pipeline = RAGPipeline(
        vector_store_directory=index_result[
            "vector_store"
        ]
    )

    # -----------------------------------------------------
    # Enable repository-specific symbol retrieval
    # -----------------------------------------------------

    from app.ai.symbol_semantic_search import (
        SymbolSemanticSearch,
    )

    pipeline.hybrid_retriever.repository_path = (
        repository
    )

    pipeline.hybrid_retriever.symbol_search = (
        SymbolSemanticSearch(
            repository_path=repository
        )
    )

    # -----------------------------------------------------
    # Retrieve combined file + symbol results
    # -----------------------------------------------------

    results = (
        pipeline.hybrid_retriever.retrieve(
            "authentication implementation",
            top_k=5,
        )
    )

    assert results

    # -----------------------------------------------------
    # Verify file-level results are still present
    # -----------------------------------------------------

    file_results = [
        embedding
        for score, embedding, distance in results
        if not embedding.metadata.get(
            "symbol_id"
        )
    ]

    assert file_results


# =========================================================
# Top-K Behaviour
# =========================================================


def test_rag_pipeline_respects_top_k_with_symbols(
    tmp_path,
):

    repository = (
        tmp_path / "sample_repo"
    )

    create_repository(repository)

    pipeline = RAGPipeline(
        vector_store_directory=str(
            tmp_path / "vector_db"
        )
    )

    from app.ai.symbol_semantic_search import (
        SymbolSemanticSearch,
    )

    pipeline.hybrid_retriever.repository_path = (
        repository
    )

    pipeline.hybrid_retriever.symbol_search = (
        SymbolSemanticSearch(
            repository_path=repository
        )
    )

    results = (
        pipeline.hybrid_retriever.retrieve(
            "authentication",
            top_k=2,
        )
    )

    assert len(results) <= 2


# =========================================================
# Repository Isolation
# =========================================================


def test_rag_pipeline_symbol_repository_isolation(
    tmp_path,
):

    repository_a = (
        tmp_path / "repo_a"
    )

    repository_b = (
        tmp_path / "repo_b"
    )

    repository_a.mkdir()
    repository_b.mkdir()

    (repository_a / "auth.py").write_text(
        """def authenticate():
    return True
""",
        encoding="utf-8",
    )

    (repository_b / "payment.py").write_text(
        """def process_payment():
    return True
""",
        encoding="utf-8",
    )

    pipeline_a = RAGPipeline(
        vector_store_directory=str(
            tmp_path / "vector_db_a"
        )
    )

    pipeline_b = RAGPipeline(
        vector_store_directory=str(
            tmp_path / "vector_db_b"
        )
    )

    from app.ai.symbol_semantic_search import (
        SymbolSemanticSearch,
    )

    # -----------------------------------------------------
    # Repository A
    # -----------------------------------------------------

    pipeline_a.hybrid_retriever.repository_path = (
        repository_a
    )

    pipeline_a.hybrid_retriever.symbol_search = (
        SymbolSemanticSearch(
            repository_path=repository_a
        )
    )

    # -----------------------------------------------------
    # Repository B
    # -----------------------------------------------------

    pipeline_b.hybrid_retriever.repository_path = (
        repository_b
    )

    pipeline_b.hybrid_retriever.symbol_search = (
        SymbolSemanticSearch(
            repository_path=repository_b
        )
    )

    # -----------------------------------------------------
    # Search Repository A
    # -----------------------------------------------------

    results_a = (
        pipeline_a.hybrid_retriever.retrieve(
            "authentication",
            top_k=5,
        )
    )

    # -----------------------------------------------------
    # Search Repository B
    # -----------------------------------------------------

    results_b = (
        pipeline_b.hybrid_retriever.retrieve(
            "payment",
            top_k=5,
        )
    )

    assert results_a
    assert results_b

    # -----------------------------------------------------
    # Extract symbol results
    # -----------------------------------------------------

    symbols_a = [
        embedding
        for score, embedding, distance in results_a
        if embedding.metadata.get(
            "symbol_id"
        )
    ]

    symbols_b = [
        embedding
        for score, embedding, distance in results_b
        if embedding.metadata.get(
            "symbol_id"
        )
    ]

    assert symbols_a
    assert symbols_b

    # -----------------------------------------------------
    # Verify repository isolation
    # -----------------------------------------------------

    for embedding in symbols_a:

        assert (
            embedding.metadata["repository"]
            == "repo_a"
        )

    for embedding in symbols_b:

        assert (
            embedding.metadata["repository"]
            == "repo_b"
        )