"""
Tests for the Repository Indexer.

Author: Harsh Aryan
Project: Cognisys
"""

from pathlib import Path

import pytest

from app.ai.repository_indexer import RepositoryIndexer


@pytest.fixture
def sample_repository(tmp_path):
    """
    Create a small temporary repository for testing.
    """

    repository = tmp_path / "sample_repo"
    repository.mkdir()

    app_dir = repository / "app"
    app_dir.mkdir()

    services_dir = app_dir / "services"
    services_dir.mkdir()

    (app_dir / "main.py").write_text(
        """
from app.services.auth import authenticate


def main():
    return authenticate()
""",
        encoding="utf-8",
    )

    (services_dir / "auth.py").write_text(
        """
def authenticate(username, password):
    return username == "admin"
""",
        encoding="utf-8",
    )

    (repository / "README.md").write_text(
        """
# Sample Repository

This is a test repository for Cognisys.
""",
        encoding="utf-8",
    )

    return repository


def test_repository_indexer_initialization(sample_repository):
    """
    RepositoryIndexer should initialize with a repository path.
    """

    indexer = RepositoryIndexer(
        repository_path=sample_repository
    )

    assert indexer.repository_path == Path(sample_repository)


def test_repository_indexer_discovers_files(sample_repository):
    """
    RepositoryIndexer should discover supported repository files.
    """

    indexer = RepositoryIndexer(
        repository_path=sample_repository
    )

    files = indexer.discover_files()

    assert len(files) > 0

    file_names = {
        file.name
        for file in files
    }

    assert "main.py" in file_names
    assert "auth.py" in file_names
    assert "README.md" in file_names


def test_repository_indexer_creates_documents(sample_repository):
    """
    RepositoryIndexer should convert repository files
    into documents suitable for chunking.
    """

    indexer = RepositoryIndexer(
        repository_path=sample_repository
    )

    documents = indexer.create_documents()

    assert len(documents) > 0

    for document in documents:
        assert "content" in document
        assert "metadata" in document


def test_repository_indexer_document_metadata(sample_repository):
    """
    Documents should contain repository file metadata.
    """

    indexer = RepositoryIndexer(
        repository_path=sample_repository
    )

    documents = indexer.create_documents()

    for document in documents:
        metadata = document["metadata"]

        assert "source" in metadata
        assert "repository" in metadata


def test_repository_indexer_generates_chunks(sample_repository):
    """
    RepositoryIndexer should generate chunks from repository documents.
    """

    indexer = RepositoryIndexer(
        repository_path=sample_repository
    )

    chunks = indexer.create_chunks()

    assert len(chunks) > 0

    for chunk in chunks:
        assert "content" in chunk
        assert "metadata" in chunk


def test_repository_indexer_generates_embeddings(sample_repository):
    """
    RepositoryIndexer should generate embeddings for repository chunks.
    """

    indexer = RepositoryIndexer(
        repository_path=sample_repository
    )

    chunks = indexer.create_chunks()

    embeddings = indexer.create_embeddings(chunks)

    assert embeddings is not None
    assert len(embeddings) == len(chunks)


def test_repository_indexer_creates_vector_store(sample_repository):
    """
    RepositoryIndexer should create a repository-specific vector store.
    """

    indexer = RepositoryIndexer(
        repository_path=sample_repository
    )

    result = indexer.index()

    assert result is not None
    assert "repository" in result
    assert "chunks" in result
    assert "embeddings" in result
    assert "vector_store" in result

    assert Path(
        result["vector_store"]
    ).exists()


def test_repository_indexer_repository_isolation(tmp_path):
    """
    Different repositories should receive different indexes.
    """

    repository_a = tmp_path / "repo_a"
    repository_b = tmp_path / "repo_b"

    repository_a.mkdir()
    repository_b.mkdir()

    (repository_a / "auth.py").write_text(
        """
def authenticate():
    return "repository A"
""",
        encoding="utf-8",
    )

    (repository_b / "payment.py").write_text(
        """
def process_payment():
    return "repository B"
""",
        encoding="utf-8",
    )

    indexer_a = RepositoryIndexer(
        repository_path=repository_a
    )

    indexer_b = RepositoryIndexer(
        repository_path=repository_b
    )

    result_a = indexer_a.index()
    result_b = indexer_b.index()

    assert result_a["repository"] != result_b["repository"]

    assert result_a["vector_store"] != result_b["vector_store"]


def test_repository_indexer_empty_repository(tmp_path):
    """
    An empty repository should be handled without crashing.
    """

    repository = tmp_path / "empty_repo"
    repository.mkdir()

    indexer = RepositoryIndexer(
        repository_path=repository
    )

    result = indexer.index()

    assert result is not None
    assert result["chunks"] == 0


def test_repository_indexer_invalid_repository():
    """
    Invalid repository paths should raise a controlled error.
    """

    with pytest.raises(ValueError):
        RepositoryIndexer(
            repository_path="C:\\does\\not\\exist\\repository"
        )


def test_repository_indexer_reindexing(sample_repository):
    """
    Indexing the same repository repeatedly should reuse
    the repository-specific index rather than creating
    unrelated duplicate indexes.
    """

    indexer = RepositoryIndexer(
        repository_path=sample_repository
    )

    first_result = indexer.index()
    second_result = indexer.index()

    assert (
        first_result["repository"]
        == second_result["repository"]
    )

    assert (
        first_result["vector_store"]
        == second_result["vector_store"]
    )