import pytest

from app.impact.impact_analyzer import ImpactAnalyzer


@pytest.fixture
def analyzer():
    dependency_graph = {
        "A": ["B"],
        "B": ["C"],
        "C": [],
    }

    return ImpactAnalyzer(dependency_graph)


def test_target_module():
    analyzer = ImpactAnalyzer({
        "A": ["B"],
        "B": ["C"],
        "C": [],
    })

    result = analyzer.analyze("C")

    assert result.target == "C"


def test_direct_dependents():
    analyzer = ImpactAnalyzer({
        "A": ["B"],
        "B": ["C"],
        "C": [],
    })

    result = analyzer.analyze("C")

    assert result.direct_dependents == ["B"]


def test_indirect_dependents():
    analyzer = ImpactAnalyzer({
        "A": ["B"],
        "B": ["C"],
        "C": [],
    })

    result = analyzer.analyze("C")

    assert result.indirect_dependents == ["A"]


def test_no_dependents():
    analyzer = ImpactAnalyzer({
        "A": ["B"],
        "B": [],
    })

    result = analyzer.analyze("A")

    assert result.direct_dependents == []
    assert result.indirect_dependents == []


def test_multiple_dependents():
    analyzer = ImpactAnalyzer({
        "A": ["C"],
        "B": ["C"],
        "C": [],
        "D": ["B"],
    })

    result = analyzer.analyze("C")

    assert sorted(result.direct_dependents) == ["A", "B"]
    assert result.indirect_dependents == ["D"]


def test_circular_dependency_does_not_loop():
    analyzer = ImpactAnalyzer({
        "A": ["B"],
        "B": ["C"],
        "C": ["A"],
    })

    result = analyzer.analyze("A")

    assert result.target == "A"
    assert set(result.direct_dependents) == {"C"}
    assert set(result.indirect_dependents) == {"B"}


def test_unknown_module():
    analyzer = ImpactAnalyzer({
        "A": ["B"],
        "B": [],
    })

    result = analyzer.analyze("X")

    assert result.target == "X"
    assert result.direct_dependents == []
    assert result.indirect_dependents == []


def test_dependencies_are_not_modified():
    graph = {
        "A": ["B"],
        "B": ["C"],
        "C": [],
    }

    analyzer = ImpactAnalyzer(graph)

    analyzer.analyze("C")

    assert graph == {
        "A": ["B"],
        "B": ["C"],
        "C": [],
    }
def test_affected_apis():
    analyzer = ImpactAnalyzer(
        {
            "app.api.users": ["app.services.users"],
            "app.services.users": ["app.database.users"],
            "app.database.users": [],
        }
    )

    result = analyzer.analyze(
        "app.database.users",
        affected_apis=["app.api.users"],
    )

    assert result.affected_apis == ["app.api.users"]


def test_affected_services():
    analyzer = ImpactAnalyzer(
        {
            "app.api.users": ["app.services.users"],
            "app.services.users": ["app.database.users"],
            "app.database.users": [],
        }
    )

    result = analyzer.analyze(
        "app.database.users",
        affected_services=["app.services.users"],
    )

    assert result.affected_services == ["app.services.users"]


def test_affected_tests():
    analyzer = ImpactAnalyzer(
        {
            "app.services.users": ["app.database.users"],
            "tests.test_users": ["app.services.users"],
            "app.database.users": [],
        }
    )

    result = analyzer.analyze(
        "app.database.users",
        affected_tests=["tests.test_users"],
    )

    assert result.affected_tests == ["tests.test_users"]

def test_low_risk_for_no_dependents():
    analyzer = ImpactAnalyzer({
        "app.database.users": [],
    })

    result = analyzer.analyze("app.database.users")

    assert result.risk == "LOW"


def test_low_risk_for_few_dependents():
    analyzer = ImpactAnalyzer({
        "app.api.users": ["app.database.users"],
        "app.database.users": [],
    })

    result = analyzer.analyze("app.database.users")

    assert result.risk == "LOW"


def test_medium_risk_for_multiple_dependents():
    analyzer = ImpactAnalyzer({
        "module_a": ["target"],
        "module_b": ["target"],
        "module_c": ["target"],
        "module_d": ["target"],
        "target": [],
    })

    result = analyzer.analyze("target")

    assert result.risk == "MEDIUM"


def test_high_risk_for_many_dependents():
    analyzer = ImpactAnalyzer({
        "module_a": ["target"],
        "module_b": ["target"],
        "module_c": ["target"],
        "module_d": ["target"],
        "module_e": ["target"],
        "module_f": ["target"],
        "module_g": ["target"],
        "target": [],
    })

    result = analyzer.analyze("target")

    assert result.risk == "HIGH"


def test_high_risk_for_circular_dependency():
    analyzer = ImpactAnalyzer({
        "A": ["B"],
        "B": ["C"],
        "C": ["A"],
    })

    result = analyzer.analyze("A")

    assert result.risk == "HIGH"


def test_high_risk_for_api_with_multiple_dependents():
    analyzer = ImpactAnalyzer({
        "app.api.users": ["target"],
        "service_a": ["target"],
        "service_b": ["target"],
        "target": [],
    })

    result = analyzer.analyze(
        "target",
        affected_apis=["app.api.users"],
    )

    assert result.risk == "HIGH"