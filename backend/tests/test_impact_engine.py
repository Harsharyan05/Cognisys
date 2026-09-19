from unittest.mock import MagicMock

from app.impact.impact_engine import ImpactEngine


def test_impact_engine_uses_architecture_engine():
    architecture_engine = MagicMock()

    architecture_engine.analyze.return_value = {
        "dependency_graph": {
            "app.api.users": ["app.services.users"],
            "app.services.users": ["app.database.users"],
            "app.database.users": [],
        }
    }

    engine = ImpactEngine(architecture_engine)

    result = engine.analyze("app.database.users")

    architecture_engine.analyze.assert_called_once()

    assert result.target == "app.database.users"
    assert result.direct_dependents == ["app.services.users"]
    assert result.indirect_dependents == ["app.api.users"]


def test_impact_engine_passes_affected_components():
    architecture_engine = MagicMock()

    architecture_engine.analyze.return_value = {
        "dependency_graph": {
            "app.api.users": ["app.services.users"],
            "app.services.users": ["app.database.users"],
            "app.database.users": [],
        }
    }

    engine = ImpactEngine(architecture_engine)

    result = engine.analyze(
        "app.database.users",
        affected_apis=["app.api.users"],
        affected_services=["app.services.users"],
        affected_tests=["tests.test_users"],
    )

    assert result.affected_apis == ["app.api.users"]
    assert result.affected_services == ["app.services.users"]
    assert result.affected_tests == ["tests.test_users"]