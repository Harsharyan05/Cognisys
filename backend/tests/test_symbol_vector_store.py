"""
Tests for the Symbol Vector Store.

Author: Harsh Aryan
Project: Cognisys
"""

from pathlib import Path

from app.ai.symbol_embedding_indexer import SymbolEmbeddingIndexer
from app.ai.multi_vector_store import MultiVectorStore


def test_symbol_embeddings_can_be_stored_and_searched(tmp_path):

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

    embedding_indexer = SymbolEmbeddingIndexer(
        repository_path=repository
    )

    embeddings = embedding_indexer.create_embeddings()

    vector_store_path = (
        tmp_path / "symbol_vector_db"
    )

    vector_store = MultiVectorStore(
        output_directory=str(vector_store_path)
    )

    vector_store.build(embeddings)

    assert (
        vector_store_path / "index.faiss"
    ).exists()

    assert (
        vector_store_path / "metadata.pkl"
    ).exists()

    assert len(vector_store.metadata) == 3
    
def test_symbol_vector_store_returns_symbol_metadata(tmp_path):

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

    embedding_indexer = SymbolEmbeddingIndexer(
        repository_path=repository
    )

    embeddings = embedding_indexer.create_embeddings()

    vector_store_path = (
        tmp_path / "symbol_vector_db"
    )

    vector_store = MultiVectorStore(
        output_directory=str(vector_store_path)
    )

    vector_store.build(embeddings)

    authenticate_embedding = next(
        embedding
        for embedding in embeddings
        if embedding.metadata["symbol_name"]
        == "authenticate"
    )

    results = vector_store.search(
        authenticate_embedding.vector,
        k=1,
    )

    assert len(results) == 1

    result_embedding, distance = results[0]

    assert result_embedding.metadata["symbol_name"] == (
        "authenticate"
    )

    assert result_embedding.metadata["symbol_type"] == (
        "method"
    )

    assert result_embedding.metadata["parent_class"] == (
        "AuthService"
    )

    assert result_embedding.metadata["symbol_id"] == (
        "auth.py:method:AuthService.authenticate"
    )    