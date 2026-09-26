"""
Tests for the Symbol Embedding Indexer.

Author: Harsh Aryan
Project: Cognisys
"""

from app.ai.symbol_embedding_indexer import SymbolEmbeddingIndexer


def test_symbol_embedding_indexer_creates_embeddings(tmp_path):

    repository = tmp_path / "sample_repo"
    repository.mkdir()

    source_file = repository / "auth.py"

    source_file.write_text(
        """class AuthService:

    def authenticate(self, username, password):
        return username == "admin"


def validate_token(token):
    return bool(token)
""",
        encoding="utf-8",
    )

    indexer = SymbolEmbeddingIndexer(
        repository_path=repository
    )

    embeddings = indexer.create_embeddings()

    assert embeddings is not None
    assert len(embeddings) == 3

    for embedding in embeddings:
        assert embedding.vector is not None
        assert embedding.dimension > 0
        assert embedding.text
        assert embedding.source_document == "auth.py"

def test_symbol_embedding_indexer_preserves_symbol_line_range(tmp_path):

    repository = tmp_path / "sample_repo"
    repository.mkdir()

    source_file = repository / "auth.py"

    source_file.write_text(
        """class AuthService:

    def authenticate(self, username, password):
        result = username == "admin"
        return result


def validate_token(token):
    return bool(token)
""",
        encoding="utf-8",
    )

    indexer = SymbolEmbeddingIndexer(
        repository_path=repository
    )

    embeddings = indexer.create_embeddings()

    auth_service = next(
        embedding
        for embedding in embeddings
        if embedding.metadata["symbol_name"] == "AuthService"
    )

    authenticate = next(
        embedding
        for embedding in embeddings
        if embedding.metadata["symbol_name"] == "authenticate"
    )

    validate_token = next(
        embedding
        for embedding in embeddings
        if embedding.metadata["symbol_name"] == "validate_token"
    )

    assert auth_service.line_start == 1
    assert auth_service.line_end == 5

    assert authenticate.line_start == 3
    assert authenticate.line_end == 5

    assert validate_token.line_start == 8
    assert validate_token.line_end == 9        