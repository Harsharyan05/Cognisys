from app.intelligence.architecture_aware_retriever import (
    ArchitectureAwareRetriever,
)


def test_dependency_query_returns_dependency_context():
    architecture = {
        "dependency_graph": {
            "app.api.users": ["app.services.users"],
            "app.services.users": ["app.database.users"],
            "app.api.auth": ["app.services.auth"],
        },
        "layers": {},
        "cycles": [],
        "hotspots": [],
        "patterns": [],
        "recommendations": [],
    }

    retriever = ArchitectureAwareRetriever(architecture)

    result = retriever.retrieve(
        "What depends on app.services.users?"
    )

    assert result["category"] == "DEPENDENCY"
    assert "app.api.users" in result["context"]


def test_hotspot_query_returns_hotspot_context():
    architecture = {
        "dependency_graph": {},
        "layers": {},
        "cycles": [],
        "hotspots": [
            {
                "module": "app.services.users",
                "fan_in": 5,
                "fan_out": 4,
                "score": 9,
                "risk": "MEDIUM",
            }
        ],
        "patterns": [],
        "recommendations": [],
    }

    retriever = ArchitectureAwareRetriever(architecture)

    result = retriever.retrieve(
        "What are the architectural hotspots?"
    )

    assert result["category"] == "HOTSPOT"
    assert "app.services.users" in result["context"]


def test_cycle_query_returns_cycle_context():
    architecture = {
        "dependency_graph": {},
        "layers": {},
        "cycles": [
            ["app.a", "app.b", "app.a"],
        ],
        "hotspots": [],
        "patterns": [],
        "recommendations": [],
    }

    retriever = ArchitectureAwareRetriever(architecture)

    result = retriever.retrieve(
        "Are there circular dependencies?"
    )

    assert result["category"] == "CYCLE"
    assert "app.a" in result["context"]


def test_pattern_query_returns_pattern_context():
    architecture = {
        "dependency_graph": {},
        "layers": {},
        "cycles": [],
        "hotspots": [],
        "patterns": [
            {
                "pattern": "Layered Architecture",
                "confidence": 0.95,
            }
        ],
        "recommendations": [],
    }

    retriever = ArchitectureAwareRetriever(architecture)

    result = retriever.retrieve(
        "What architecture patterns are used?"
    )

    assert result["category"] == "PATTERN"
    assert "Layered Architecture" in result["context"]


def test_risk_query_returns_recommendation_context():
    architecture = {
        "dependency_graph": {},
        "layers": {},
        "cycles": [],
        "hotspots": [],
        "patterns": [],
        "recommendations": [
            {
                "title": "High Coupling Detected",
                "severity": "HIGH",
                "description": "Reduce coupling between modules.",
            }
        ],
    }

    retriever = ArchitectureAwareRetriever(architecture)

    result = retriever.retrieve(
        "What architectural risks should I know about?"
    )

    assert result["category"] == "RISK"
    assert "High Coupling Detected" in result["context"]


def test_unknown_query_returns_general_architecture_context():
    architecture = {
        "dependency_graph": {},
        "layers": {
            "Presentation": ["app.api"],
            "Business": ["app.services"],
        },
        "cycles": [],
        "hotspots": [],
        "patterns": [],
        "recommendations": [],
    }

    retriever = ArchitectureAwareRetriever(architecture)

    result = retriever.retrieve(
        "How is this repository structured?"
    )

    assert result["category"] == "GENERAL"
    assert "Presentation" in result["context"]