"""
Tests for HybridRetriever symbol-level retrieval integration.

Author: Harsh Aryan
Project: Cognisys
"""

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


def test_hybrid_retriever_can_use_symbol_search(tmp_path):

    repository = tmp_path / "sample_repo"
    create_repository(repository)

    retriever = HybridRetriever(
        repository_path=repository
    )

    results = retriever.retrieve(
        "where is user authentication implemented?",
        top_k=5,
    )

    assert results


def test_hybrid_retriever_returns_symbol_metadata(tmp_path):

    repository = tmp_path / "sample_repo"
    create_repository(repository)

    retriever = HybridRetriever(
        repository_path=repository
    )

    results = retriever.retrieve(
        "authenticate user",
        top_k=5,
    )

    assert results

    symbol_results = [
        result
        for result in results
        if result[1].metadata.get("symbol_id")
    ]

    assert symbol_results

    score, embedding, distance = symbol_results[0]

    metadata = embedding.metadata

    assert metadata["symbol_name"] == "authenticate"

    assert metadata["symbol_type"] == "method"

    assert metadata["parent_class"] == "AuthService"


def test_hybrid_retriever_preserves_file_level_results(
    tmp_path,
):

    repository = tmp_path / "sample_repo"
    create_repository(repository)

    retriever = HybridRetriever(
        repository_path=repository
    )

    results = retriever.retrieve(
        "authentication implementation",
        top_k=5,
    )

    assert results

    file_results = [
        result
        for result in results
        if not result[1].metadata.get("symbol_id")
    ]

    assert file_results


def test_hybrid_retriever_respects_top_k(tmp_path):

    repository = tmp_path / "sample_repo"
    create_repository(repository)

    retriever = HybridRetriever(
        repository_path=repository
    )

    results = retriever.retrieve(
        "authentication",
        top_k=2,
    )

    assert len(results) <= 2


def test_hybrid_retriever_handles_empty_query(tmp_path):

    repository = tmp_path / "sample_repo"
    create_repository(repository)

    retriever = HybridRetriever(
        repository_path=repository
    )

    results = retriever.retrieve(
        "",
        top_k=5,
    )

    assert results == []


def test_hybrid_retriever_repository_isolation(tmp_path):

    repository_a = tmp_path / "repo_a"
    repository_b = tmp_path / "repo_b"

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

    retriever_a = HybridRetriever(
        repository_path=repository_a
    )

    retriever_b = HybridRetriever(
        repository_path=repository_b
    )

    results_a = retriever_a.retrieve(
        "authentication",
        top_k=5,
    )

    results_b = retriever_b.retrieve(
        "payment",
        top_k=5,
    )

    assert results_a
    assert results_b

    # Only inspect symbol-level results because
    # repository metadata is guaranteed for symbols.

    symbol_results_a = [
        embedding
        for score, embedding, distance in results_a
        if embedding.metadata.get("symbol_id")
    ]

    symbol_results_b = [
        embedding
        for score, embedding, distance in results_b
        if embedding.metadata.get("symbol_id")
    ]

    assert symbol_results_a
    assert symbol_results_b

    for embedding in symbol_results_a:

        assert (
            embedding.metadata["repository"]
            == "repo_a"
        )

    for embedding in symbol_results_b:

        assert (
            embedding.metadata["repository"]
            == "repo_b"
        )


def test_symbol_retrieval_failure_does_not_break_file_search(
    tmp_path,
):

    repository = tmp_path / "sample_repo"
    create_repository(repository)

    retriever = HybridRetriever(
        repository_path=repository
    )

    # Disable symbol retrieval.
    retriever.symbol_search = None

    results = retriever.retrieve(
        "authentication",
        top_k=5,
    )

    assert results