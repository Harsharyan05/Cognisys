from unittest.mock import MagicMock

from app.intelligence.intelligence_engine import IntelligenceEngine
from app.intelligence.unified_context import UnifiedContext


# ============================================================
# RAG
# ============================================================

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

    result = engine.ask(
        "What does UserService do?"
    )

    assert result["category"] == "RAG"
    assert result["answer"] == (
        "UserService handles user operations."
    )

    rag_pipeline.ask.assert_called_once()
    architecture_engine.analyze.assert_not_called()


# ============================================================
# ARCHITECTURE
# ============================================================

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

    result = engine.ask(
        "Which layer does UserService belong to?"
    )

    assert result["category"] == "ARCHITECTURE"
    assert "Business" in result["architecture"]["layers"]

    architecture_engine.analyze.assert_called_once()
    rag_pipeline.ask.assert_not_called()


# ============================================================
# BOTH
# ============================================================

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
        "Explain the authentication flow and "
        "what happens if I modify AuthService."
    )

    assert result["category"] == "BOTH"
    assert result["answer"] == (
        "AuthService handles authentication."
    )

    assert result["architecture"]["layers"]["Business"] == [
        "app/services"
    ]

    rag_pipeline.ask.assert_called_once()
    architecture_engine.analyze.assert_called_once()


# ============================================================
# EXISTING UNIFIED CONTEXT
# ============================================================

def test_both_question_creates_architecture_context():
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
        "Explain the authentication flow and "
        "what happens if I modify AuthService."
    )

    assert result["category"] == "BOTH"

    assert result["architecture_context"] is not None

    assert result["architecture_context"].analysis[
        "layers"
    ]["Business"] == ["app/services"]


# ============================================================
# IMPACT
# ============================================================

def test_both_question_runs_impact_analysis():
    rag_pipeline = MagicMock()
    architecture_engine = MagicMock()
    impact_engine = MagicMock()

    rag_pipeline.ask.return_value = {
        "answer": (
            "Changing the database module may affect "
            "the user service."
        ),
        "citations": [],
    }

    architecture_engine.analyze.return_value = {
        "layers": {},
        "dependency_graph": {
            "app.api.users": [
                "app.services.users"
            ],
            "app.services.users": [
                "app.database.users"
            ],
            "app.database.users": [],
        },
        "cycles": [],
        "hotspots": [],
        "patterns": [],
        "recommendations": [],
    }

    impact_engine.analyze.return_value = {
        "target": "app.database.users",
        "direct_dependents": [
            "app.services.users"
        ],
        "indirect_dependents": [
            "app.api.users"
        ],
        "affected_apis": [
            "app.api.users"
        ],
        "affected_services": [
            "app.services.users"
        ],
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
    assert result["impact"]["target"] == (
        "app.database.users"
    )
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


# ============================================================
# UNIFIED CONTEXT INTEGRATION
# ============================================================

def test_both_creates_unified_context():
    rag_pipeline = MagicMock()
    architecture_engine = MagicMock()

    rag_pipeline.ask.return_value = {
        "answer": (
            "Authentication uses the auth service."
        ),
        "raw_answer": (
            "Authentication uses the auth service."
        ),
        "citations": [],
        "rag_context": [],
    }

    architecture_engine.analyze.return_value = {
        "layers": {
            "Presentation": ["app/api"],
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

    result = engine.ask(
        "Explain the authentication flow."
    )

    assert result["category"] == "BOTH"

    assert "unified_context" in result

    assert isinstance(
        result["unified_context"],
        UnifiedContext,
    )


def test_unified_context_contains_architecture_context():
    rag_pipeline = MagicMock()
    architecture_engine = MagicMock()

    rag_pipeline.ask.return_value = {
        "answer": "Authentication flow.",
        "raw_answer": "Authentication flow.",
        "citations": [],
        "rag_context": [],
    }

    architecture_engine.analyze.return_value = {
        "layers": {
            "Presentation": ["app/api"],
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

    result = engine.ask(
        "Explain the authentication flow."
    )

    unified_context = result["unified_context"]

    assert (
        unified_context.get_architecture_context()
        is result["architecture_context"]
    )


def test_unified_context_contains_rag_context():
    rag_pipeline = MagicMock()
    architecture_engine = MagicMock()

    rag_context = [
        {
            "document": "auth.py",
            "content": "Authentication logic.",
            "score": 0.95,
        }
    ]

    rag_pipeline.ask.return_value = {
        "answer": "Authentication flow.",
        "raw_answer": "Authentication flow.",
        "citations": [],
        "rag_context": rag_context,
    }

    architecture_engine.analyze.return_value = {
        "layers": {},
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

    result = engine.ask(
        "Explain the authentication flow."
    )

    unified_context = result["unified_context"]

    assert (
        unified_context.get_rag_context()
        == rag_context
    )


def test_impact_is_added_to_unified_context():
    rag_pipeline = MagicMock()
    architecture_engine = MagicMock()
    impact_engine = MagicMock()

    rag_pipeline.ask.return_value = {
        "answer": (
            "The change may affect dependent modules."
        ),
        "raw_answer": (
            "The change may affect dependent modules."
        ),
        "citations": [],
        "rag_context": [],
    }

    architecture_engine.analyze.return_value = {
        "layers": {},
        "dependency_graph": {},
        "cycles": [],
        "hotspots": [],
        "patterns": [],
        "recommendations": [],
    }

    impact_engine.analyze.return_value = {
        "target": "app/services/auth_service.py",
        "direct_dependents": [
            "app/api/auth.py"
        ],
        "indirect_dependents": [],
        "affected_apis": [],
        "affected_services": [],
        "affected_tests": [],
        "risk": "MEDIUM",
    }

    engine = IntelligenceEngine(
        rag_pipeline=rag_pipeline,
        architecture_engine=architecture_engine,
        impact_engine=impact_engine,
    )

    result = engine.ask(
        "What happens if I modify "
        "app/services/auth_service.py?"
    )

    unified_context = result["unified_context"]

    assert (
        unified_context.get_impact_context()
        == result["impact"]
    )
    
def create_test_engine():
    rag_pipeline = MagicMock()
    architecture_engine = MagicMock()
    impact_engine = MagicMock()

    rag_pipeline.ask.return_value = {
        "answer": "Test answer",
        "raw_answer": "Test raw answer",
        "citations": [],
        "rag_context": [],
        "performance": None,
        "conversation_size": 0,
    }

    architecture_engine.analyze.return_value = {
        "layers": {
            "Business": ["app/services"],
            "Presentation": ["app/api"],
        },
        "dependency_graph": {
            "app.api.auth": [
                "app.services.auth_service"
            ],
        },
        "cycles": [],
        "hotspots": [
            {
                "module": "app.services.auth_service",
                "fan_in": 5,
                "fan_out": 2,
                "score": 12,
                "risk": "HIGH",
            }
        ],
        "patterns": [
            {
                "pattern": "Layered Architecture",
                "confidence": 0.95,
            }
        ],
        "recommendations": [
            {
                "message": "Review high-risk hotspot.",
                "severity": "HIGH",
            }
        ],
    }

    return IntelligenceEngine(
        rag_pipeline=rag_pipeline,
        architecture_engine=architecture_engine,
        impact_engine=impact_engine,
    )


def test_architecture_question_contains_architecture_citations():
    engine = create_test_engine()

    result = engine.ask(
        "What architecture does this repository use?"
    )

    assert "architecture_citations" in result
    assert result["architecture_citations"]


def test_both_question_contains_architecture_citations():
    engine = create_test_engine()

    result = engine.ask(
        "What happens if I modify "
        "app/services/auth_services.py? "
    )
    assert result["category"] == "BOTH"
    assert "architecture_citations" in result
    assert result["architecture_citations"]


def test_architecture_citations_have_valid_types():
    engine = create_test_engine()

    result = engine.ask(
        "What are the architecture hotspots?"
    )

    citations = result["architecture_citations"]

    assert citations

    valid_types = {
        "architecture_layer",
        "architecture_dependency",
        "architecture_cycle",
        "architecture_hotspot",
        "architecture_pattern",
        "architecture_recommendation",
    }

    for citation in citations:
        assert citation["type"] in valid_types


def test_architecture_citations_have_stable_ids():
    engine = create_test_engine()

    result = engine.ask(
        "What are the architecture dependencies?"
    )

    citations = result["architecture_citations"]

    assert citations

    for citation in citations:
        assert citation["id"].startswith("ARCH-")   