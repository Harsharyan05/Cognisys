import pytest

from app.architecture.hotspot_detector import Hotspot
from app.architecture.architecture_models import ArchitecturePattern
from app.architecture.recommendation_engine import RecommendationEngine


# ---------------------------------------------------------
# Helper
# ---------------------------------------------------------

def get_recommendation(recommendations, title):
    for recommendation in recommendations:
        if recommendation.title == title:
            return recommendation
    return None


# ---------------------------------------------------------
# Initialization
# ---------------------------------------------------------

def test_engine_initialization():
    hotspots = []
    cycles = []
    patterns = []

    engine = RecommendationEngine(
        hotspots,
        cycles,
        patterns,
    )

    assert engine.hotspots == hotspots
    assert engine.cycles == cycles
    assert engine.patterns == patterns


# ---------------------------------------------------------
# Empty Input
# ---------------------------------------------------------

def test_empty_inputs_generate_no_recommendations():
    engine = RecommendationEngine(
        hotspots=[],
        cycles=[],
        patterns=[],
    )

    recommendations = engine.generate()

    assert recommendations == []


# ---------------------------------------------------------
# Hotspot Recommendations
# ---------------------------------------------------------

def test_high_risk_hotspot_generates_high_priority_recommendation():
    hotspot = Hotspot(
        module="app.services.user_service",
        fan_in=8,
        fan_out=5,
        score=13,
        risk="HIGH",
    )

    engine = RecommendationEngine(
        hotspots=[hotspot],
        cycles=[],
        patterns=[],
    )

    recommendations = engine.generate()

    recommendation = get_recommendation(
        recommendations,
        "High Coupling Detected",
    )

    assert recommendation is not None
    assert recommendation.priority == "HIGH"
    assert recommendation.module == "app.services.user_service"


def test_high_risk_hotspot_recommendation_message():
    hotspot = Hotspot(
        module="app.services.user_service",
        fan_in=8,
        fan_out=5,
        score=13,
        risk="HIGH",
    )

    engine = RecommendationEngine(
        hotspots=[hotspot],
        cycles=[],
        patterns=[],
    )

    recommendations = engine.generate()

    recommendation = get_recommendation(
        recommendations,
        "High Coupling Detected",
    )

    assert recommendation is not None
    assert (
        recommendation.recommendation
        == "Split this module into smaller services to reduce coupling."
    )


def test_medium_risk_hotspot_generates_medium_priority_recommendation():
    hotspot = Hotspot(
        module="app.services.analysis_service",
        fan_in=3,
        fan_out=3,
        score=6,
        risk="MEDIUM",
    )

    engine = RecommendationEngine(
        hotspots=[hotspot],
        cycles=[],
        patterns=[],
    )

    recommendations = engine.generate()

    recommendation = get_recommendation(
        recommendations,
        "Medium Coupling",
    )

    assert recommendation is not None
    assert recommendation.priority == "MEDIUM"
    assert recommendation.module == "app.services.analysis_service"


def test_medium_risk_hotspot_recommendation_message():
    hotspot = Hotspot(
        module="app.services.analysis_service",
        fan_in=3,
        fan_out=3,
        score=6,
        risk="MEDIUM",
    )

    engine = RecommendationEngine(
        hotspots=[hotspot],
        cycles=[],
        patterns=[],
    )

    recommendations = engine.generate()

    recommendation = get_recommendation(
        recommendations,
        "Medium Coupling",
    )

    assert recommendation is not None
    assert (
        recommendation.recommendation
        == "Consider refactoring this module if it continues to grow."
    )


def test_low_risk_hotspot_generates_no_hotspot_recommendation():
    hotspot = Hotspot(
        module="app.utils.helper",
        fan_in=1,
        fan_out=1,
        score=2,
        risk="LOW",
    )

    engine = RecommendationEngine(
        hotspots=[hotspot],
        cycles=[],
        patterns=[],
    )

    recommendations = engine.generate()

    assert recommendations == []


def test_multiple_hotspots_generate_multiple_recommendations():
    hotspots = [
        Hotspot(
            module="module.high",
            fan_in=8,
            fan_out=5,
            score=13,
            risk="HIGH",
        ),
        Hotspot(
            module="module.medium",
            fan_in=3,
            fan_out=3,
            score=6,
            risk="MEDIUM",
        ),
        Hotspot(
            module="module.low",
            fan_in=1,
            fan_out=1,
            score=2,
            risk="LOW",
        ),
    ]

    engine = RecommendationEngine(
        hotspots=hotspots,
        cycles=[],
        patterns=[],
    )

    recommendations = engine.generate()

    assert len(recommendations) == 2

    titles = [r.title for r in recommendations]

    assert "High Coupling Detected" in titles
    assert "Medium Coupling" in titles


# ---------------------------------------------------------
# Circular Dependency Recommendations
# ---------------------------------------------------------

def test_cycle_generates_high_priority_recommendation():
    cycle = [
        "app.a",
        "app.b",
        "app.a",
    ]

    engine = RecommendationEngine(
        hotspots=[],
        cycles=[cycle],
        patterns=[],
    )

    recommendations = engine.generate()

    recommendation = get_recommendation(
        recommendations,
        "Circular Dependency",
    )

    assert recommendation is not None
    assert recommendation.priority == "HIGH"
    assert recommendation.module == "app.a"


def test_cycle_recommendation_message():
    cycle = [
        "app.a",
        "app.b",
        "app.a",
    ]

    engine = RecommendationEngine(
        hotspots=[],
        cycles=[cycle],
        patterns=[],
    )

    recommendations = engine.generate()

    recommendation = get_recommendation(
        recommendations,
        "Circular Dependency",
    )

    assert recommendation is not None
    assert (
        recommendation.recommendation
        == "Break this circular dependency using interfaces or dependency inversion."
    )


def test_multiple_cycles_generate_multiple_recommendations():
    cycles = [
        ["app.a", "app.b", "app.a"],
        ["app.x", "app.y", "app.x"],
    ]

    engine = RecommendationEngine(
        hotspots=[],
        cycles=cycles,
        patterns=[],
    )

    recommendations = engine.generate()

    cycle_recommendations = [
        r for r in recommendations
        if r.title == "Circular Dependency"
    ]

    assert len(cycle_recommendations) == 2
    assert cycle_recommendations[0].module == "app.a"
    assert cycle_recommendations[1].module == "app.x"


# ---------------------------------------------------------
# Pattern Recommendations
# ---------------------------------------------------------

def test_layered_architecture_generates_recommendation():
    pattern = ArchitecturePattern(
        name="Layered Architecture",
        confidence=0.95,
        evidence=[
            "Presentation layer detected",
            "Business layer detected",
            "Persistence layer detected",
        ],
    )

    engine = RecommendationEngine(
        hotspots=[],
        cycles=[],
        patterns=[pattern],
    )

    recommendations = engine.generate()

    recommendation = get_recommendation(
        recommendations,
        "Architecture Pattern",
    )

    assert recommendation is not None
    assert recommendation.priority == "LOW"
    assert recommendation.module == "Repository"


def test_layered_architecture_recommendation_message():
    pattern = ArchitecturePattern(
        name="Layered Architecture",
        confidence=0.95,
        evidence=[],
    )

    engine = RecommendationEngine(
        hotspots=[],
        cycles=[],
        patterns=[pattern],
    )

    recommendations = engine.generate()

    recommendation = get_recommendation(
        recommendations,
        "Architecture Pattern",
    )

    assert recommendation is not None
    assert (
        recommendation.recommendation
        == "Layered architecture detected. Continue enforcing layer separation."
    )


def test_monolithic_architecture_generates_recommendation():
    pattern = ArchitecturePattern(
        name="Monolithic Architecture",
        confidence=0.85,
        evidence=[
            "25 modules detected",
            "Single deployable project",
        ],
    )

    engine = RecommendationEngine(
        hotspots=[],
        cycles=[],
        patterns=[pattern],
    )

    recommendations = engine.generate()

    recommendation = get_recommendation(
        recommendations,
        "Scalability",
    )

    assert recommendation is not None
    assert recommendation.priority == "LOW"
    assert recommendation.module == "Repository"


def test_monolithic_architecture_recommendation_message():
    pattern = ArchitecturePattern(
        name="Monolithic Architecture",
        confidence=0.85,
        evidence=[],
    )

    engine = RecommendationEngine(
        hotspots=[],
        cycles=[],
        patterns=[pattern],
    )

    recommendations = engine.generate()

    recommendation = get_recommendation(
        recommendations,
        "Scalability",
    )

    assert recommendation is not None
    assert (
        recommendation.recommendation
        == "Consider modularization or microservices as the project grows."
    )


def test_mvc_alone_generates_no_pattern_recommendation():
    pattern = ArchitecturePattern(
        name="MVC",
        confidence=0.60,
        evidence=[
            "Presentation layer detected",
            "Persistence layer detected",
        ],
    )

    engine = RecommendationEngine(
        hotspots=[],
        cycles=[],
        patterns=[pattern],
    )

    recommendations = engine.generate()

    assert recommendations == []


# ---------------------------------------------------------
# Combined Recommendations
# ---------------------------------------------------------

def test_all_recommendation_types_are_generated():
    hotspot = Hotspot(
        module="app.core",
        fan_in=8,
        fan_out=5,
        score=13,
        risk="HIGH",
    )

    cycle = [
        "app.a",
        "app.b",
        "app.a",
    ]

    patterns = [
        ArchitecturePattern(
            name="Layered Architecture",
            confidence=0.95,
            evidence=[],
        ),
        ArchitecturePattern(
            name="Monolithic Architecture",
            confidence=0.85,
            evidence=[],
        ),
    ]

    engine = RecommendationEngine(
        hotspots=[hotspot],
        cycles=[cycle],
        patterns=patterns,
    )

    recommendations = engine.generate()

    assert len(recommendations) == 4

    titles = [r.title for r in recommendations]

    assert "High Coupling Detected" in titles
    assert "Circular Dependency" in titles
    assert "Architecture Pattern" in titles
    assert "Scalability" in titles


# ---------------------------------------------------------
# Recommendation Model
# ---------------------------------------------------------

def test_recommendation_fields_are_populated():
    hotspot = Hotspot(
        module="app.test",
        fan_in=10,
        fan_out=2,
        score=12,
        risk="HIGH",
    )

    engine = RecommendationEngine(
        hotspots=[hotspot],
        cycles=[],
        patterns=[],
    )

    recommendations = engine.generate()

    recommendation = recommendations[0]

    assert recommendation.priority == "HIGH"
    assert recommendation.title == "High Coupling Detected"
    assert recommendation.module == "app.test"
    assert recommendation.recommendation