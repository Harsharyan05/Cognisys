from unittest.mock import Mock

from app.intelligence.intelligence_engine import IntelligenceEngine


def test_both_question_uses_architecture_context():
    rag_pipeline = Mock()
    architecture_engine = Mock()

    architecture_engine.analyze.return_value = {
        "layers": {
            "Presentation": ["app.api"],
            "Business": ["app.services"],
        },
        "dependency_graph": {
            "app.api": ["app.services"],
        },
        "cycles": [],
        "hotspots": [],
        "patterns": [],
        "recommendations": [],
    }

    rag_pipeline.ask.return_value = {
        "answer": "Authentication flows through the API and service layers.",
        "raw_answer": "Authentication flows through the API and service layers.",
        "citations": [],
        "performance": {},
        "conversation_size": 1,
    }

    engine = IntelligenceEngine(
        rag_pipeline=rag_pipeline,
        architecture_engine=architecture_engine,
    )

    result = engine.ask(
        "Explain the authentication flow."
    )

    assert result["category"] == "BOTH"

    rag_pipeline.ask.assert_called_once()

    call_kwargs = rag_pipeline.ask.call_args.kwargs

    assert "architecture_context" in call_kwargs
    assert call_kwargs["architecture_context"] is not None


def test_impact_question_still_uses_architecture_context():
    rag_pipeline = Mock()
    architecture_engine = Mock()
    impact_engine = Mock()

    architecture_engine.analyze.return_value = {
        "layers": {},
        "dependency_graph": {
            "app.api.users": ["app.services.users"],
        },
        "cycles": [],
        "hotspots": [],
        "patterns": [],
        "recommendations": [],
    }

    rag_pipeline.ask.return_value = {
        "answer": "Changing the service may affect the API.",
        "raw_answer": "Changing the service may affect the API.",
        "citations": [],
        "performance": {},
        "conversation_size": 1,
    }

    impact_engine.analyze.return_value = {
        "target": "app.services.users",
        "direct_dependents": ["app.api.users"],
        "indirect_dependents": [],
        "affected_apis": [],
        "affected_services": [],
        "affected_tests": [],
        "risk": "LOW",
    }

    engine = IntelligenceEngine(
        rag_pipeline=rag_pipeline,
        architecture_engine=architecture_engine,
        impact_engine=impact_engine,
    )

    result = engine.ask(
        "What happens if I modify app.services.users?"
    )

    assert result["category"] == "BOTH"
    assert "impact" in result

    rag_pipeline.ask.assert_called_once()

    call_kwargs = rag_pipeline.ask.call_args.kwargs

    assert "architecture_context" in call_kwargs
    assert call_kwargs["architecture_context"] is not None

    impact_engine.analyze.assert_called_once_with(
        "app.services.users"
    )