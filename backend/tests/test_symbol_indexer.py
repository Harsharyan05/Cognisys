"""
Tests for the Symbol Indexer.

Author: Harsh Aryan
Project: Cognisys
"""

from app.ai.symbol_indexer import SymbolIndexer


def test_symbol_indexer_creates_symbol_chunks(tmp_path):

    repository = tmp_path / "sample_repo"
    repository.mkdir()

    app_dir = repository / "app"
    app_dir.mkdir()

    source_file = app_dir / "auth.py"

    source_file.write_text(
        """class AuthService:

    def authenticate(self, username, password):
        return username == "admin"


def validate_token(token):
    return bool(token)
""",
        encoding="utf-8",
    )

    indexer = SymbolIndexer(
        repository_path=repository
    )

    chunks = indexer.create_symbol_chunks()

    assert chunks is not None
    assert len(chunks) == 3

    symbol_names = {
        chunk["metadata"]["symbol_name"]
        for chunk in chunks
    }

    assert "AuthService" in symbol_names
    assert "authenticate" in symbol_names
    assert "validate_token" in symbol_names

def test_symbol_indexer_preserves_symbol_metadata(tmp_path):

    repository = tmp_path / "sample_repo"
    repository.mkdir()

    app_dir = repository / "app"
    app_dir.mkdir()

    source_file = app_dir / "auth.py"

    source_file.write_text(
        """class AuthService:

    def authenticate(self, username, password):
        return username == "admin"


def validate_token(token):
    return bool(token)
""",
        encoding="utf-8",
    )

    indexer = SymbolIndexer(
        repository_path=repository
    )

    chunks = indexer.create_symbol_chunks()

    auth_service = next(
        chunk
        for chunk in chunks
        if chunk["metadata"]["symbol_name"] == "AuthService"
    )

    authenticate = next(
        chunk
        for chunk in chunks
        if chunk["metadata"]["symbol_name"] == "authenticate"
    )

    validate_token = next(
        chunk
        for chunk in chunks
        if chunk["metadata"]["symbol_name"] == "validate_token"
    )

    assert auth_service["metadata"]["repository"] == "sample_repo"
    assert auth_service["metadata"]["source"] == "app\\auth.py"
    assert auth_service["metadata"]["symbol_type"] == "class"
    assert auth_service["metadata"]["symbol_id"] == (
        "app\\auth.py:class:AuthService"
    )
    assert auth_service["metadata"]["line"] == 1

    assert authenticate["metadata"]["symbol_type"] == "method"
    assert authenticate["metadata"]["parent_class"] == "AuthService"
    assert authenticate["metadata"]["line"] == 3

    assert validate_token["metadata"]["symbol_type"] == "function"
    assert validate_token["metadata"]["parent_class"] is None  

def test_symbol_indexer_keeps_repositories_isolated(tmp_path):

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

    (repository_b / "auth.py").write_text(
        """def authenticate():
    return "repository B"
""",
        encoding="utf-8",
    )

    indexer_a = SymbolIndexer(
        repository_path=repository_a
    )

    indexer_b = SymbolIndexer(
        repository_path=repository_b
    )

    chunks_a = indexer_a.create_symbol_chunks()
    chunks_b = indexer_b.create_symbol_chunks()

    assert len(chunks_a) == 1
    assert len(chunks_b) == 1

    assert (
        chunks_a[0]["metadata"]["repository"]
        == "repo_a"
    )

    assert (
        chunks_b[0]["metadata"]["repository"]
        == "repo_b"
    )

    assert (
        chunks_a[0]["content"]
        != chunks_b[0]["content"]
    )      