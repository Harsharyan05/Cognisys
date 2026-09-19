from unittest.mock import MagicMock

from app.impact.impact_analyzer import ImpactAnalyzer


def test_impact_analyzer_uses_architecture_dependency_graph():
    architecture_engine = MagicMock()

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

    analysis = architecture_engine.analyze()

    dependency_graph = analysis["dependency_graph"]

    analyzer = ImpactAnalyzer(dependency_graph)

    result = analyzer.analyze("app.database.users")

    assert result.target == "app.database.users"
    assert result.direct_dependents == ["app.services.users"]
    assert result.indirect_dependents == ["app.api.users"]


def test_impact_analysis_preserves_architecture_graph():
    architecture_engine = MagicMock()

    dependency_graph = {
        "app.api.users": ["app.services.users"],
        "app.services.users": ["app.database.users"],
        "app.database.users": [],
    }

    architecture_engine.analyze.return_value = {
        "dependency_graph": dependency_graph,
    }

    analysis = architecture_engine.analyze()

    analyzer = ImpactAnalyzer(
        analysis["dependency_graph"]
    )

    analyzer.analyze("app.database.users")

    assert analysis["dependency_graph"] == dependency_graph