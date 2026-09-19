from unittest.mock import Mock

from app.intelligence.intelligence_engine import IntelligenceEngine


def test_architecture_question_uses_architecture_aware_retriever():
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

    engine = IntelligenceEngine(
        rag_pipeline=rag_pipeline,
        architecture_engine=architecture_engine,
    )

    result = engine.ask(
        "What are the dependencies of app.api?"
    )

    assert result["category"] == "ARCHITECTURE"

    assert "architecture_context" in result
    assert result["architecture_context"] is not None

    assert "app.api" in result["architecture_context"].get(
        "context"
    )