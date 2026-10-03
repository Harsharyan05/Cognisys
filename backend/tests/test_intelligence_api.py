"""
Tests for the Intelligence API.

Author: Harsh Aryan
Project: Cognisys
"""

from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


# ============================================================
# RAG
# ============================================================


@patch("app.api.v1.intelligence.RepositoryIndexer")
@patch("app.api.v1.intelligence.RepositoryService.clone_repository")
@patch("app.api.v1.intelligence.IntelligenceEngine")
def test_intelligence_ask_rag(
    mock_engine,
    mock_clone,
    mock_indexer,
    tmp_path,
):
    repository_path = tmp_path / "demo"
    repository_path.mkdir()

    mock_clone.return_value = {
        "status": "success",
        "repository_name": "demo",
        "local_path": str(repository_path),
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
        str(repository_path)
    )

    mock_indexer.return_value.index.assert_called_once()

    mock_engine.return_value.ask.assert_called_once_with(
        "What does the authentication service do?"
    )


# ============================================================
# INVALID URL
# ============================================================


def test_intelligence_ask_invalid_url():
    response = client.post(
        "/api/v1/intelligence/ask",
        json={
            "repository_url": "not-a-valid-url",
            "question": "Explain the repository.",
        },
    )

    assert response.status_code == 422


# ============================================================
# EMPTY QUESTION
# ============================================================


def test_intelligence_ask_empty_question():
    response = client.post(
        "/api/v1/intelligence/ask",
        json={
            "repository_url": "https://github.com/example/demo",
            "question": "",
        },
    )

    assert response.status_code == 422


# ============================================================
# ARCHITECTURE
# ============================================================


@patch("app.api.v1.intelligence.RepositoryIndexer")
@patch("app.api.v1.intelligence.RepositoryService.clone_repository")
@patch("app.api.v1.intelligence.IntelligenceEngine")
def test_intelligence_ask_architecture(
    mock_engine,
    mock_clone,
    mock_indexer,
    tmp_path,
):
    repository_path = tmp_path / "demo"
    repository_path.mkdir()

    mock_clone.return_value = {
        "status": "success",
        "repository_name": "demo",
        "local_path": str(repository_path),
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
        str(repository_path)
    )

    mock_indexer.return_value.index.assert_called_once()

    mock_engine.return_value.ask.assert_called_once_with(
        "What is the architecture of this repository?"
    )


# ============================================================
# BOTH
# ============================================================


@patch("app.api.v1.intelligence.RepositoryIndexer")
@patch("app.api.v1.intelligence.RepositoryService.clone_repository")
@patch("app.api.v1.intelligence.IntelligenceEngine")
def test_intelligence_ask_both(
    mock_engine,
    mock_clone,
    mock_indexer,
    tmp_path,
):
    repository_path = tmp_path / "demo"
    repository_path.mkdir()

    mock_clone.return_value = {
        "status": "success",
        "repository_name": "demo",
        "local_path": str(repository_path),
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
        str(repository_path)
    )

    mock_indexer.return_value.index.assert_called_once()

    mock_engine.return_value.ask.assert_called_once_with(
        "Explain the authentication flow."
    )


# ============================================================
# IMPACT
# ============================================================


@patch("app.api.v1.intelligence.RepositoryIndexer")
@patch("app.api.v1.intelligence.RepositoryService.clone_repository")
@patch("app.api.v1.intelligence.IntelligenceEngine")
def test_intelligence_ask_impact(
    mock_engine,
    mock_clone,
    mock_indexer,
    tmp_path,
):
    repository_path = tmp_path / "demo"
    repository_path.mkdir()

    mock_clone.return_value = {
        "status": "success",
        "repository_name": "demo",
        "local_path": str(repository_path),
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
        str(repository_path)
    )

    mock_indexer.return_value.index.assert_called_once()

    mock_engine.return_value.ask.assert_called_once_with(
        "What happens if I modify app/services/auth_service.py?"
    )


# ============================================================
# INDEXING BEFORE RAG
# ============================================================


@patch("app.api.v1.intelligence.RepositoryIndexer")
@patch("app.api.v1.intelligence.RepositoryService.clone_repository")
@patch("app.api.v1.intelligence.RAGPipeline")
@patch("app.api.v1.intelligence.IntelligenceEngine")
def test_intelligence_ask_indexes_repository_before_rag(
    mock_engine,
    mock_rag_pipeline,
    mock_clone,
    mock_indexer,
    tmp_path,
):
    repository_path = tmp_path / "demo"
    repository_path.mkdir()

    mock_clone.return_value = {
        "status": "success",
        "repository_name": "demo",
        "local_path": str(repository_path),
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
        str(repository_path)
    )

    mock_indexer.return_value.index.assert_called_once()

    mock_rag_pipeline.assert_called_once_with(
        vector_store_directory=(
            "storage/repositories/demo/vector_db"
        ),
        repository_path=str(repository_path),
    )


# ============================================================
# GRAPH INTELLIGENCE
# ============================================================


@patch("app.api.v1.intelligence.CodeGraphEngine")
@patch("app.api.v1.intelligence.GraphQuery")
@patch("app.api.v1.intelligence.GraphAwareQuery")
@patch("app.api.v1.intelligence.RepositoryIndexer")
@patch("app.api.v1.intelligence.RepositoryService.clone_repository")
@patch("app.api.v1.intelligence.RAGPipeline")
@patch("app.api.v1.intelligence.IntelligenceEngine")
def test_intelligence_ask_wires_graph_intelligence(
    mock_engine,
    mock_rag_pipeline,
    mock_clone,
    mock_indexer,
    mock_graph_aware_query,
    mock_graph_query,
    mock_graph_engine,
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

    mock_graph_engine_instance = MagicMock()
    mock_graph_engine.return_value = (
        mock_graph_engine_instance
    )

    mock_graph = MagicMock()
    mock_graph_engine_instance.build.return_value = mock_graph

    mock_graph_query_instance = MagicMock()
    mock_graph_query.return_value = (
        mock_graph_query_instance
    )

    mock_graph_aware_query_instance = MagicMock()
    mock_graph_aware_query.return_value = (
        mock_graph_aware_query_instance
    )

    mock_engine.return_value.ask.return_value = {
        "category": "BOTH",
        "answer": (
            "AuthService.authenticate is called "
            "by AuthController.login."
        ),
        "raw_answer": (
            "AuthService.authenticate is called "
            "by AuthController.login."
        ),
        "citations": [],
        "graph_query_context": {
            "callers": [
                "controller.py:method:"
                "AuthController.login"
            ]
        },
    }

    response = client.post(
        "/api/v1/intelligence/ask",
        json={
            "repository_url": (
                "https://github.com/example/demo"
            ),
            "question": (
                "Who calls "
                "service.py:method:"
                "AuthService.authenticate?"
            ),
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"
    assert data["category"] == "BOTH"

    mock_graph_engine.assert_called_once_with(
        "C:\\repo\\demo"
    )

    mock_graph_engine_instance.build.assert_called_once()

    mock_graph_query.assert_called_once_with(
        mock_graph
    )

    mock_graph_aware_query.assert_called_once_with(
        mock_graph_query_instance
    )


# ============================================================
# GRAPH COMPONENT INJECTION
# ============================================================


@patch("app.api.v1.intelligence.CodeGraphEngine")
@patch("app.api.v1.intelligence.GraphQuery")
@patch("app.api.v1.intelligence.GraphAwareQuery")
@patch("app.api.v1.intelligence.RepositoryIndexer")
@patch("app.api.v1.intelligence.RepositoryService.clone_repository")
@patch("app.api.v1.intelligence.RAGPipeline")
@patch("app.api.v1.intelligence.IntelligenceEngine")
def test_intelligence_engine_receives_graph_components(
    mock_engine,
    mock_rag_pipeline,
    mock_clone,
    mock_indexer,
    mock_graph_aware_query,
    mock_graph_query,
    mock_graph_engine,
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

    graph_engine = mock_graph_engine.return_value
    graph = MagicMock()

    graph_engine.build.return_value = graph

    graph_query = mock_graph_query.return_value
    graph_aware_query = mock_graph_aware_query.return_value

    mock_engine.return_value.ask.return_value = {
        "category": "BOTH",
        "answer": "Graph answer.",
        "raw_answer": "Graph answer.",
        "citations": [],
    }

    response = client.post(
        "/api/v1/intelligence/ask",
        json={
            "repository_url": (
                "https://github.com/example/demo"
            ),
            "question": (
                "Who calls "
                "service.py:method:"
                "AuthService.authenticate?"
            ),
        },
    )

    assert response.status_code == 200

    mock_engine.assert_called_once()

    _, kwargs = mock_engine.call_args

    assert kwargs["code_graph_engine"] is graph_engine
    assert kwargs["graph_aware_query"] is graph_aware_query