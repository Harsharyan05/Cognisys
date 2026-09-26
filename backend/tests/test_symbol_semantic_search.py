"""
Tests for Symbol Semantic Search.

Author: Harsh Aryan
Project: Cognisys
"""

from pathlib import Path

from app.ai.symbol_semantic_search import SymbolSemanticSearch


def create_repository(repository_path):
    """
    Create a small repository used by the tests.
    """

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


def test_symbol_semantic_search_finds_relevant_symbol(tmp_path):

    repository = tmp_path / "sample_repo"
    create_repository(repository)

    search = SymbolSemanticSearch(
        repository_path=repository
    )

    results = search.search(
        "authenticate user credentials",
        top_k=1,
    )

    assert results
    assert len(results) == 1

    embedding, distance = results[0]

    assert embedding.metadata["symbol_name"] == (
        "authenticate"
    )

    assert embedding.metadata["symbol_type"] == (
        "method"
    )

    assert embedding.metadata["parent_class"] == (
        "AuthService"
    )


def test_symbol_semantic_search_handles_empty_query(tmp_path):

    repository = tmp_path / "sample_repo"
    create_repository(repository)

    search = SymbolSemanticSearch(
        repository_path=repository
    )

    results = search.search(
        "",
        top_k=5,
    )

    assert results == []


def test_symbol_semantic_search_handles_whitespace_query(tmp_path):

    repository = tmp_path / "sample_repo"
    create_repository(repository)

    search = SymbolSemanticSearch(
        repository_path=repository
    )

    results = search.search(
        "   ",
        top_k=5,
    )

    assert results == []


def test_symbol_semantic_search_respects_top_k(tmp_path):

    repository = tmp_path / "sample_repo"
    create_repository(repository)

    search = SymbolSemanticSearch(
        repository_path=repository
    )

    results = search.search(
        "authentication security",
        top_k=2,
    )

    assert len(results) <= 2


def test_symbol_semantic_search_preserves_source_metadata(tmp_path):

    repository = tmp_path / "sample_repo"
    create_repository(repository)

    search = SymbolSemanticSearch(
        repository_path=repository
    )

    results = search.search(
        "authenticate",
        top_k=1,
    )

    assert results

    embedding, distance = results[0]

    assert embedding.source_document == "auth.py"
    assert embedding.metadata["source"] == "auth.py"
    assert embedding.metadata["symbol_id"] == (
        "auth.py:method:AuthService.authenticate"
    )


def test_symbol_semantic_search_preserves_line_range(tmp_path):

    repository = tmp_path / "sample_repo"
    create_repository(repository)

    search = SymbolSemanticSearch(
        repository_path=repository
    )

    results = search.search(
        "authenticate",
        top_k=1,
    )

    assert results

    embedding, distance = results[0]

    assert embedding.line_start == 3
    assert embedding.line_end == 4


def test_symbol_semantic_search_repository_isolation(tmp_path):

    repository_a = tmp_path / "repo_a"
    repository_b = tmp_path / "repo_b"

    repository_a.mkdir()
    repository_b.mkdir()

    (repository_a / "auth.py").write_text(
        """def authenticate():
    return "repository A"
""",
        encoding="utf-8",
    )

    (repository_b / "payment.py").write_text(
        """def process_payment():
    return "repository B"
""",
        encoding="utf-8",
    )

    search_a = SymbolSemanticSearch(
        repository_path=repository_a
    )

    search_b = SymbolSemanticSearch(
        repository_path=repository_b
    )

    results_a = search_a.search(
        "authentication",
        top_k=5,
    )

    results_b = search_b.search(
        "payment",
        top_k=5,
    )

    assert results_a
    assert results_b

    for embedding, distance in results_a:
        assert (
            embedding.metadata["repository"]
            == "repo_a"
        )

    for embedding, distance in results_b:
        assert (
            embedding.metadata["repository"]
            == "repo_b"
        )


def test_symbol_semantic_search_uses_custom_vector_store(
    tmp_path,
):

    repository = tmp_path / "sample_repo"
    create_repository(repository)

    vector_store_directory = (
        tmp_path / "custom_symbol_vector_db"
    )

    search = SymbolSemanticSearch(
        repository_path=repository,
        vector_store_directory=str(
            vector_store_directory
        ),
    )

    assert (
        search.vector_store.output_directory
        == Path(vector_store_directory)
    )

    assert (
        vector_store_directory / "index.faiss"
    ).exists()

    assert (
        vector_store_directory / "metadata.pkl"
    ).exists()