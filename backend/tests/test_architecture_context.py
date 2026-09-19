import pytest
from app.intelligence.architecture_context import ArchitectureContext

@pytest.fixture
def architecture_analysis():
    return {
        "layers": {
            "Presentation": ["app/api"],
            "Business": ["app/services"],
        },
        "dependency_graph": {
            "app/api/router.py": ["app/services/user_service.py"],
            "app/services/user_service.py": [],
        },
        "cycles": [],
        "hotspots": [],
        "patterns": [
            {
                "name": "Layered Architecture",
                "confidence": 0.95,
            }
        ],
        "recommendations": [],
    }


def test_architecture_context_initialization(architecture_analysis):
    context = ArchitectureContext(architecture_analysis)

    assert context.analysis == architecture_analysis


def test_get_layers(architecture_analysis):
    context = ArchitectureContext(architecture_analysis)

    assert context.get_layers() == {
        "Presentation": ["app/api"],
        "Business": ["app/services"],
    }


def test_get_dependency_graph(architecture_analysis):
    context = ArchitectureContext(architecture_analysis)

    graph = context.get_dependency_graph()

    assert graph["app/api/router.py"] == [
        "app/services/user_service.py"
    ]


def test_get_cycles(architecture_analysis):
    context = ArchitectureContext(architecture_analysis)

    assert context.get_cycles() == []


def test_get_patterns(architecture_analysis):
    context = ArchitectureContext(architecture_analysis)

    patterns = context.get_patterns()

    assert patterns[0]["name"] == "Layered Architecture"


def test_get_hotspots(architecture_analysis):
    context = ArchitectureContext(architecture_analysis)

    assert context.get_hotspots() == []


def test_get_recommendations(architecture_analysis):
    context = ArchitectureContext(architecture_analysis)

    assert context.get_recommendations() == []