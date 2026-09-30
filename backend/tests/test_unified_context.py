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


# ============================================================
# INITIALIZATION
# ============================================================

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


# ============================================================
# RAG CONTEXT
# ============================================================

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


def test_empty_rag_context(architecture_context):
    context = UnifiedContext(
        rag_context=[],
        architecture_context=architecture_context,
    )

    assert context.get_rag_context() == []


# ============================================================
# ARCHITECTURE CONTEXT
# ============================================================

def test_get_architecture_context(architecture_context):
    context = UnifiedContext(
        rag_context=[],
        architecture_context=architecture_context,
    )

    assert context.get_architecture_context() is architecture_context


def test_architecture_context_preserves_analysis(
    architecture_context,
):
    context = UnifiedContext(
        rag_context=[],
        architecture_context=architecture_context,
    )

    architecture = context.get_architecture_context()

    assert architecture is architecture_context
    assert architecture.analysis["layers"]["Presentation"] == [
        "app/api"
    ]
    assert architecture.analysis["layers"]["Business"] == [
        "app/services"
    ]


# ============================================================
# COMBINED CONTEXT
# ============================================================

def test_unified_context_contains_rag_and_architecture(
    architecture_context,
):
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
    assert (
        context.get_architecture_context()
        is architecture_context
    )


# ============================================================
# EMPTY CONTEXT
# ============================================================

def test_unified_context_with_empty_contexts():
    context = UnifiedContext(
        rag_context=[],
        architecture_context=None,
    )

    assert context.get_rag_context() == []
    assert context.get_architecture_context() is None


# ============================================================
# RAG CONTEXT MULTIPLE RESULTS
# ============================================================

def test_rag_context_preserves_multiple_results(
    architecture_context,
):
    rag_context = [
        {
            "document": "auth.py",
            "content": "Authentication logic.",
            "score": 0.95,
        },
        {
            "document": "user_service.py",
            "content": "User service logic.",
            "score": 0.89,
        },
        {
            "document": "router.py",
            "content": "API routing logic.",
            "score": 0.82,
        },
    ]

    context = UnifiedContext(
        rag_context=rag_context,
        architecture_context=architecture_context,
    )

    results = context.get_rag_context()

    assert len(results) == 3
    assert results[0]["document"] == "auth.py"
    assert results[1]["document"] == "user_service.py"
    assert results[2]["document"] == "router.py"


# ============================================================
# CONTEXT IDENTITY
# ============================================================

def test_unified_context_does_not_modify_rag_context(
    architecture_context,
):
    rag_context = [
        {
            "document": "auth.py",
            "content": "Authentication logic.",
            "score": 0.95,
        }
    ]

    original_rag_context = list(rag_context)

    context = UnifiedContext(
        rag_context=rag_context,
        architecture_context=architecture_context,
    )

    assert context.get_rag_context() == original_rag_context
    
def test_architecture_citations_are_stored():
    citations = [
        {
            "id": "ARCH-LAYER-001",
            "type": "architecture_layer",
        }
    ]

    context = UnifiedContext(
        architecture_citations=citations
    )

    assert context.get_architecture_citations() == citations


def test_architecture_citations_default_to_empty_list():
    context = UnifiedContext()

    assert context.get_architecture_citations() == []


def test_architecture_citations_are_preserved():
    citations = [
        {
            "id": "ARCH-DEP-001",
            "type": "architecture_dependency",
        },
        {
            "id": "ARCH-HOTSPOT-001",
            "type": "architecture_hotspot",
        },
    ]

    context = UnifiedContext(
        architecture_citations=citations
    )

    assert len(
        context.get_architecture_citations()
    ) == 2


def test_architecture_citations_are_in_to_dict():
    citations = [
        {
            "id": "ARCH-LAYER-001",
            "type": "architecture_layer",
        }
    ]

    context = UnifiedContext(
        architecture_citations=citations
    )

    result = context.to_dict()

    assert result["architecture_citations"] == citations    