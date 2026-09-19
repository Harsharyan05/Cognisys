from unittest.mock import MagicMock

from app.intelligence.intelligence_engine import IntelligenceEngine


def test_rag_question_uses_rag_pipeline():
    rag_pipeline = MagicMock()
    architecture_engine = MagicMock()

    rag_pipeline.ask.return_value = {
        "answer": "UserService handles user operations.",
        "citations": [],
    }

    engine = IntelligenceEngine(
        rag_pipeline=rag_pipeline,
        architecture_engine=architecture_engine,
    )

    result = engine.ask("What does UserService do?")

    assert result["category"] == "RAG"
    assert result["answer"] == "UserService handles user operations."

    rag_pipeline.ask.assert_called_once()
    architecture_engine.analyze.assert_not_called()


def test_architecture_question_uses_architecture_engine():
    rag_pipeline = MagicMock()
    architecture_engine = MagicMock()

    architecture_engine.analyze.return_value = {
        "layers": {
            "Business": ["app/services"],
        },
        "dependency_graph": {},
        "cycles": [],
        "hotspots": [],
        "patterns": [],
        "recommendations": [],
    }

    engine = IntelligenceEngine(
        rag_pipeline=rag_pipeline,
        architecture_engine=architecture_engine,
    )

    result = engine.ask("Which layer does UserService belong to?")

    assert result["category"] == "ARCHITECTURE"
    assert "Business" in result["architecture"]["layers"]

    architecture_engine.analyze.assert_called_once()
    rag_pipeline.ask.assert_not_called()


def test_both_question_uses_rag_and_architecture():
    rag_pipeline = MagicMock()
    architecture_engine = MagicMock()

    rag_pipeline.ask.return_value = {
        "answer": "AuthService handles authentication.",
        "citations": [],
    }

    architecture_engine.analyze.return_value = {
        "layers": {
            "Business": ["app/services"],
        },
        "dependency_graph": {
            "app/api/auth.py": ["app/services/auth_service.py"],
        },
        "cycles": [],
        "hotspots": [],
        "patterns": [],
        "recommendations": [],
    }

    engine = IntelligenceEngine(
        rag_pipeline=rag_pipeline,
        architecture_engine=architecture_engine,
    )

    result = engine.ask(
        "Explain the authentication flow and what happens if I modify AuthService."
    )

    assert result["category"] == "BOTH"
    assert result["answer"] == "AuthService handles authentication."
    assert result["architecture"]["layers"]["Business"] == [
        "app/services"
    ]

    rag_pipeline.ask.assert_called_once()
    architecture_engine.analyze.assert_called_once()

def test_both_question_creates_unified_context():
    rag_pipeline = MagicMock()
    architecture_engine = MagicMock()

    rag_pipeline.ask.return_value = {
        "answer": "AuthService handles authentication.",
        "citations": [],
    }

    architecture_engine.analyze.return_value = {
        "layers": {
            "Business": ["app/services"],
        },
        "dependency_graph": {
            "app/api/auth.py": [
                "app/services/auth_service.py"
            ],
        },
        "cycles": [],
        "hotspots": [],
        "patterns": [],
        "recommendations": [],
    }

    engine = IntelligenceEngine(
        rag_pipeline=rag_pipeline,
        architecture_engine=architecture_engine,
    )

    result = engine.ask(
        "Explain the authentication flow and what happens if I modify AuthService."
    )

    assert result["category"] == "BOTH"

    assert result["architecture_context"] is not None
    assert result["architecture_context"].analysis[
        "layers"
    ]["Business"] == ["app/services"]    

def test_both_question_runs_impact_analysis():
    rag_pipeline = MagicMock()
    architecture_engine = MagicMock()

    rag_pipeline.ask.return_value = {
        "answer": "Changing the database module may affect the user service.",
        "citations": [],
    }

    architecture_engine.analyze.return_value = {
        "layers": {},
        "dependency_graph": {
            "app.api.users": ["app.services.users"],
            "app.services.users": ["app.database.users"],
            "app.database.users": [],
        },
        "cycles": [],
        "hotspots": [],
        "patterns": [],
        "recommendations": [],
    }

    impact_engine = MagicMock()

    impact_engine.analyze.return_value = {
        "target": "app.database.users",
        "direct_dependents": ["app.services.users"],
        "indirect_dependents": ["app.api.users"],
        "affected_apis": ["app.api.users"],
        "affected_services": ["app.services.users"],
        "affected_tests": [],
        "risk": "HIGH",
    }

    engine = IntelligenceEngine(
        rag_pipeline=rag_pipeline,
        architecture_engine=architecture_engine,
        impact_engine=impact_engine,
    )

    result = engine.ask(
        "What happens if I modify app.database.users?"
    )

    assert result["category"] == "BOTH"
    assert result["impact"]["target"] == "app.database.users"
    assert result["impact"]["risk"] == "HIGH"

    impact_engine.analyze.assert_called_once_with(
        "app.database.users"
    )


def test_non_impact_question_does_not_run_impact_analysis():
    rag_pipeline = MagicMock()
    architecture_engine = MagicMock()
    impact_engine = MagicMock()

    rag_pipeline.ask.return_value = {
        "answer": "UserService handles user operations.",
        "citations": [],
    }

    engine = IntelligenceEngine(
        rag_pipeline=rag_pipeline,
        architecture_engine=architecture_engine,
        impact_engine=impact_engine,
    )

    result = engine.ask(
        "What does UserService do?"
    )

    assert result["category"] == "RAG"

    impact_engine.analyze.assert_not_called()