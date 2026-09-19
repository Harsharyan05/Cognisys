import pytest

from app.intelligence.architecture_context import ArchitectureContext
from app.intelligence.unified_context import UnifiedContext


@pytest.fixture
def architecture_context():
    analysis = {
        "layers": {
            "Presentation": ["app/api"],
            "Business": ["app/services"],
        },
        "dependency_graph": {
            "app/api/router.py": ["app/services/user_service.py"],
        },
        "cycles": [],
        "hotspots": [],
        "patterns": [],
        "recommendations": [],
    }

    return ArchitectureContext(analysis)


def test_unified_context_initialization(architecture_context):
    rag_context = [
        {
            "document": "services.md",
            "content": "UserService handles user operations.",
            "score": 0.91,
        }
    ]

    context = UnifiedContext(
        rag_context=rag_context,
        architecture_context=architecture_context,
    )

    assert context.rag_context == rag_context
    assert context.architecture_context == architecture_context


def test_get_rag_context(architecture_context):
    rag_context = [
        {
            "document": "services.md",
            "content": "UserService handles user operations.",
            "score": 0.91,
        }
    ]

    context = UnifiedContext(
        rag_context=rag_context,
        architecture_context=architecture_context,
    )

    assert context.get_rag_context() == rag_context


def test_get_architecture_context(architecture_context):
    context = UnifiedContext(
        rag_context=[],
        architecture_context=architecture_context,
    )

    assert context.get_architecture_context() is architecture_context


def test_empty_rag_context(architecture_context):
    context = UnifiedContext(
        rag_context=[],
        architecture_context=architecture_context,
    )

    assert context.get_rag_context() == []