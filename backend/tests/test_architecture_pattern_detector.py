import pytest

from app.architecture.architecture_pattern_detector import (
    ArchitecturePatternDetector,
)


# ---------------------------------------------------------
# Helper
# ---------------------------------------------------------

def get_pattern(patterns, name):
    for pattern in patterns:
        if pattern.name == name:
            return pattern
    return None


# ---------------------------------------------------------
# Initialization
# ---------------------------------------------------------

def test_detector_initialization():
    layers = {"Presentation": ["api.py"]}
    graph = {"main": ["api"]}

    detector = ArchitecturePatternDetector(layers, graph)

    assert detector.layers == layers
    assert detector.graph == graph


# ---------------------------------------------------------
# Layered Architecture
# ---------------------------------------------------------

def test_layered_architecture_detected():
    layers = {
        "Presentation": ["api"],
        "Business": ["services"],
        "Persistence": ["database"],
    }

    detector = ArchitecturePatternDetector(layers, {})

    patterns = detector.detect()

    pattern = get_pattern(patterns, "Layered Architecture")

    assert pattern is not None
    assert pattern.confidence == 0.95


def test_layered_architecture_requires_all_layers():
    layers = {
        "Presentation": ["api"],
        "Business": ["services"],
    }

    detector = ArchitecturePatternDetector(layers, {})

    patterns = detector.detect()

    assert get_pattern(patterns, "Layered Architecture") is None


def test_layered_architecture_missing_presentation():
    layers = {
        "Business": ["services"],
        "Persistence": ["database"],
    }

    detector = ArchitecturePatternDetector(layers, {})

    patterns = detector.detect()

    assert get_pattern(patterns, "Layered Architecture") is None


def test_layered_architecture_missing_business():
    layers = {
        "Presentation": ["api"],
        "Persistence": ["database"],
    }

    detector = ArchitecturePatternDetector(layers, {})

    patterns = detector.detect()

    assert get_pattern(patterns, "Layered Architecture") is None


def test_layered_architecture_missing_persistence():
    layers = {
        "Presentation": ["api"],
        "Business": ["services"],
    }

    detector = ArchitecturePatternDetector(layers, {})

    patterns = detector.detect()

    assert get_pattern(patterns, "Layered Architecture") is None


def test_layered_architecture_evidence():
    layers = {
        "Presentation": ["api"],
        "Business": ["services"],
        "Persistence": ["database"],
    }

    detector = ArchitecturePatternDetector(layers, {})

    patterns = detector.detect()

    pattern = get_pattern(patterns, "Layered Architecture")

    assert pattern is not None

    assert "Business layer detected" in pattern.evidence
    assert "Persistence layer detected" in pattern.evidence
    assert "Presentation layer detected" in pattern.evidence


# ---------------------------------------------------------
# MVC
# ---------------------------------------------------------

def test_mvc_detected_with_presentation_and_persistence():
    layers = {
        "Presentation": ["api"],
        "Persistence": ["models"],
    }

    detector = ArchitecturePatternDetector(layers, {})

    patterns = detector.detect()

    pattern = get_pattern(patterns, "MVC")

    assert pattern is not None
    assert pattern.confidence == 0.60


def test_mvc_requires_presentation():
    layers = {
        "Persistence": ["models"],
    }

    detector = ArchitecturePatternDetector(layers, {})

    patterns = detector.detect()

    assert get_pattern(patterns, "MVC") is None


def test_mvc_requires_persistence():
    layers = {
        "Presentation": ["api"],
    }

    detector = ArchitecturePatternDetector(layers, {})

    patterns = detector.detect()

    assert get_pattern(patterns, "MVC") is None


def test_mvc_evidence():
    layers = {
        "Presentation": ["api"],
        "Persistence": ["models"],
    }

    detector = ArchitecturePatternDetector(layers, {})

    patterns = detector.detect()

    pattern = get_pattern(patterns, "MVC")

    assert pattern is not None

    assert "Presentation layer detected" in pattern.evidence
    assert "Persistence layer detected" in pattern.evidence


# ---------------------------------------------------------
# Monolithic Architecture
# ---------------------------------------------------------

def test_monolith_detected_above_20_modules():
    graph = {
        f"module_{i}": []
        for i in range(21)
    }

    detector = ArchitecturePatternDetector({}, graph)

    patterns = detector.detect()

    pattern = get_pattern(patterns, "Monolithic Architecture")

    assert pattern is not None
    assert pattern.confidence == 0.85


def test_monolith_not_detected_at_20_modules():
    graph = {
        f"module_{i}": []
        for i in range(20)
    }

    detector = ArchitecturePatternDetector({}, graph)

    patterns = detector.detect()

    assert get_pattern(patterns, "Monolithic Architecture") is None


def test_monolith_not_detected_below_20_modules():
    graph = {
        f"module_{i}": []
        for i in range(10)
    }

    detector = ArchitecturePatternDetector({}, graph)

    patterns = detector.detect()

    assert get_pattern(patterns, "Monolithic Architecture") is None


def test_monolith_evidence():
    graph = {
        f"module_{i}": []
        for i in range(25)
    }

    detector = ArchitecturePatternDetector({}, graph)

    patterns = detector.detect()

    pattern = get_pattern(patterns, "Monolithic Architecture")

    assert pattern is not None

    assert "25 modules detected" in pattern.evidence
    assert "Single deployable project" in pattern.evidence


# ---------------------------------------------------------
# Multiple Patterns
# ---------------------------------------------------------

def test_multiple_patterns_detected():
    layers = {
        "Presentation": ["api"],
        "Business": ["services"],
        "Persistence": ["database"],
    }

    graph = {
        f"module_{i}": []
        for i in range(21)
    }

    detector = ArchitecturePatternDetector(layers, graph)

    patterns = detector.detect()

    names = [pattern.name for pattern in patterns]

    assert "Layered Architecture" in names
    assert "MVC" in names
    assert "Monolithic Architecture" in names


# ---------------------------------------------------------
# Empty Architecture
# ---------------------------------------------------------

def test_no_patterns_for_empty_architecture():
    detector = ArchitecturePatternDetector({}, {})

    patterns = detector.detect()

    assert patterns == []