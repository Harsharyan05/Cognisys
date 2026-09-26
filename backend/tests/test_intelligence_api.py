"""
Tests for the Intelligence API.

Author: Harsh Aryan
Project: Cognisys
"""

from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


@patch("app.api.v1.intelligence.RepositoryIndexer")
@patch("app.api.v1.intelligence.RepositoryService.clone_repository")
@patch("app.api.v1.intelligence.IntelligenceEngine")
def test_intelligence_ask_rag(
    mock_engine,
    mock_clone,
    mock_indexer,
):
    mock_clone.return_value = {
        "status": "success",
        "repository_name": "demo",
        "local_path": "C:\\repo\\demo",
    }

    mock_indexer.return_value.index.return_value = {
        "repository": "demo",
        "chunks": 10,
        "embeddings": 10,
        "vector_store": "storage/repositories/demo/vector_db",
    }

    mock_engine.return_value.ask.return_value = {
        "category": "RAG",
        "answer": "Authentication is handled by the auth service.",
        "raw_answer": "Authentication is handled by the auth service.",
        "citations": [],
    }

    response = client.post(
        "/api/v1/intelligence/ask",
        json={
            "repository_url": "https://github.com/example/demo",
            "question": "What does the authentication service do?",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"
    assert data["category"] == "RAG"
    assert data["answer"] == (
        "Authentication is handled by the auth service."
    )

    mock_clone.assert_called_once_with(
        "https://github.com/example/demo"
    )

    mock_indexer.assert_called_once_with(
        "C:\\repo\\demo"
    )

    mock_indexer.return_value.index.assert_called_once()

    mock_engine.return_value.ask.assert_called_once_with(
        "What does the authentication service do?"
    )


def test_intelligence_ask_invalid_url():
    response = client.post(
        "/api/v1/intelligence/ask",
        json={
            "repository_url": "not-a-valid-url",
            "question": "Explain the repository.",
        },
    )

    assert response.status_code == 422


def test_intelligence_ask_empty_question():
    response = client.post(
        "/api/v1/intelligence/ask",
        json={
            "repository_url": "https://github.com/example/demo",
            "question": "",
        },
    )

    assert response.status_code == 422


@patch("app.api.v1.intelligence.RepositoryIndexer")
@patch("app.api.v1.intelligence.RepositoryService.clone_repository")
@patch("app.api.v1.intelligence.IntelligenceEngine")
def test_intelligence_ask_architecture(
    mock_engine,
    mock_clone,
    mock_indexer,
):
    mock_clone.return_value = {
        "status": "success",
        "repository_name": "demo",
        "local_path": "C:\\repo\\demo",
    }

    mock_indexer.return_value.index.return_value = {
        "repository": "demo",
        "chunks": 10,
        "embeddings": 10,
        "vector_store": "storage/repositories/demo/vector_db",
    }

    mock_engine.return_value.ask.return_value = {
        "category": "ARCHITECTURE",
        "architecture": {
            "layers": {
                "Presentation": ["app/api"],
                "Business": ["app/services"],
            }
        },
        "architecture_context": {
            "category": "GENERAL",
            "context": "Presentation: app/api",
        },
    }

    response = client.post(
        "/api/v1/intelligence/ask",
        json={
            "repository_url": "https://github.com/example/demo",
            "question": "What is the architecture of this repository?",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"
    assert data["category"] == "ARCHITECTURE"
    assert "architecture" in data
    assert "architecture_context" in data

    mock_clone.assert_called_once_with(
        "https://github.com/example/demo"
    )

    mock_indexer.assert_called_once_with(
        "C:\\repo\\demo"
    )

    mock_indexer.return_value.index.assert_called_once()

    mock_engine.return_value.ask.assert_called_once_with(
        "What is the architecture of this repository?"
    )


@patch("app.api.v1.intelligence.RepositoryIndexer")
@patch("app.api.v1.intelligence.RepositoryService.clone_repository")
@patch("app.api.v1.intelligence.IntelligenceEngine")
def test_intelligence_ask_both(
    mock_engine,
    mock_clone,
    mock_indexer,
):
    mock_clone.return_value = {
        "status": "success",
        "repository_name": "demo",
        "local_path": "C:\\repo\\demo",
    }

    mock_indexer.return_value.index.return_value = {
        "repository": "demo",
        "chunks": 10,
        "embeddings": 10,
        "vector_store": "storage/repositories/demo/vector_db",
    }

    mock_engine.return_value.ask.return_value = {
        "category": "BOTH",
        "answer": (
            "Authentication flows through the API "
            "and service layers."
        ),
        "raw_answer": (
            "Authentication flows through the API "
            "and service layers."
        ),
        "citations": [],
        "architecture": {
            "layers": {
                "Presentation": ["app/api"],
                "Business": ["app/services"],
            }
        },
        "architecture_context": {},
    }

    response = client.post(
        "/api/v1/intelligence/ask",
        json={
            "repository_url": "https://github.com/example/demo",
            "question": "Explain the authentication flow.",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"
    assert data["category"] == "BOTH"
    assert "answer" in data
    assert "architecture" in data

    mock_clone.assert_called_once_with(
        "https://github.com/example/demo"
    )

    mock_indexer.assert_called_once_with(
        "C:\\repo\\demo"
    )

    mock_indexer.return_value.index.assert_called_once()

    mock_engine.return_value.ask.assert_called_once_with(
        "Explain the authentication flow."
    )


@patch("app.api.v1.intelligence.RepositoryIndexer")
@patch("app.api.v1.intelligence.RepositoryService.clone_repository")
@patch("app.api.v1.intelligence.IntelligenceEngine")
def test_intelligence_ask_impact(
    mock_engine,
    mock_clone,
    mock_indexer,
):
    mock_clone.return_value = {
        "status": "success",
        "repository_name": "demo",
        "local_path": "C:\\repo\\demo",
    }

    mock_indexer.return_value.index.return_value = {
        "repository": "demo",
        "chunks": 10,
        "embeddings": 10,
        "vector_store": "storage/repositories/demo/vector_db",
    }

    mock_engine.return_value.ask.return_value = {
        "category": "BOTH",
        "answer": (
            "Changing the authentication service may "
            "affect dependent modules."
        ),
        "raw_answer": (
            "Changing the authentication service may "
            "affect dependent modules."
        ),
        "citations": [],
        "architecture": {},
        "architecture_context": {},
        "impact": {
            "target": "app/services/auth_service.py",
            "direct_dependents": [
                "app/api/auth.py"
            ],
            "indirect_dependents": [],
            "affected_apis": [],
            "affected_services": [],
            "affected_tests": [],
            "risk": "MEDIUM",
        },
    }

    response = client.post(
        "/api/v1/intelligence/ask",
        json={
            "repository_url": "https://github.com/example/demo",
            "question": (
                "What happens if I modify "
                "app/services/auth_service.py?"
            ),
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"
    assert data["category"] == "BOTH"
    assert "impact" in data

    assert data["impact"]["target"] == (
        "app/services/auth_service.py"
    )

    assert data["impact"]["risk"] == "MEDIUM"

    mock_clone.assert_called_once_with(
        "https://github.com/example/demo"
    )

    mock_indexer.assert_called_once_with(
        "C:\\repo\\demo"
    )

    mock_indexer.return_value.index.assert_called_once()

    mock_engine.return_value.ask.assert_called_once_with(
        "What happens if I modify app/services/auth_service.py?"
    )


@patch("app.api.v1.intelligence.RepositoryIndexer")
@patch("app.api.v1.intelligence.RepositoryService.clone_repository")
@patch("app.api.v1.intelligence.RAGPipeline")
@patch("app.api.v1.intelligence.IntelligenceEngine")
def test_intelligence_ask_indexes_repository_before_rag(
    mock_engine,
    mock_rag_pipeline,
    mock_clone,
    mock_indexer,
):
    mock_clone.return_value = {
        "status": "success",
        "repository_name": "demo",
        "local_path": "C:\\repo\\demo",
    }

    mock_indexer.return_value.index.return_value = {
        "repository": "demo",
        "chunks": 10,
        "embeddings": 10,
        "vector_store": (
            "storage/repositories/demo/vector_db"
        ),
    }

    mock_engine.return_value.ask.return_value = {
        "category": "RAG",
        "answer": (
            "Authentication is handled by the auth service."
        ),
        "raw_answer": (
            "Authentication is handled by the auth service."
        ),
        "citations": [],
    }

    response = client.post(
        "/api/v1/intelligence/ask",
        json={
            "repository_url": "https://github.com/example/demo",
            "question": "What does the authentication service do?",
        },
    )

    assert response.status_code == 200

    mock_clone.assert_called_once_with(
        "https://github.com/example/demo"
    )

    mock_indexer.assert_called_once_with(
        "C:\\repo\\demo"
    )

    mock_indexer.return_value.index.assert_called_once()

    mock_rag_pipeline.assert_called_once_with(
        vector_store_directory=(
            "storage/repositories/demo/vector_db"
        )
    )