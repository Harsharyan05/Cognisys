from app.architecture.circular_dependency_detector import (
    CircularDependencyDetector,
)


def test_initialization():
    graph = {
        "A": ["B"],
        "B": ["C"],
        "C": [],
    }

    detector = CircularDependencyDetector(graph)

    assert detector.graph == graph
    assert detector.visited == set()
    assert detector.recursion_stack == set()
    assert detector.path == []
    assert detector.cycles == []


def test_no_circular_dependencies():
    graph = {
        "A": ["B"],
        "B": ["C"],
        "C": [],
    }

    detector = CircularDependencyDetector(graph)

    cycles = detector.detect()

    assert cycles == []


def test_simple_circular_dependency():
    graph = {
        "A": ["B"],
        "B": ["A"],
    }

    detector = CircularDependencyDetector(graph)

    cycles = detector.detect()

    assert cycles == [["A", "B", "A"]]


def test_three_node_circular_dependency():
    graph = {
        "A": ["B"],
        "B": ["C"],
        "C": ["A"],
    }

    detector = CircularDependencyDetector(graph)

    cycles = detector.detect()

    assert ["A", "B", "C", "A"] in cycles


def test_four_node_circular_dependency():
    graph = {
        "A": ["B"],
        "B": ["C"],
        "C": ["D"],
        "D": ["A"],
    }

    detector = CircularDependencyDetector(graph)

    cycles = detector.detect()

    assert ["A", "B", "C", "D", "A"] in cycles


def test_cycle_with_non_cyclic_dependency():
    graph = {
        "A": ["B"],
        "B": ["C"],
        "C": ["A", "D"],
        "D": [],
    }

    detector = CircularDependencyDetector(graph)

    cycles = detector.detect()

    assert ["A", "B", "C", "A"] in cycles
    assert len(cycles) == 1


def test_multiple_independent_cycles():
    graph = {
        "A": ["B"],
        "B": ["A"],
        "C": ["D"],
        "D": ["C"],
    }

    detector = CircularDependencyDetector(graph)

    cycles = detector.detect()

    assert ["A", "B", "A"] in cycles
    assert ["C", "D", "C"] in cycles
    assert len(cycles) == 2


def test_self_dependency():
    graph = {
        "A": ["A"],
    }

    detector = CircularDependencyDetector(graph)

    cycles = detector.detect()

    assert cycles == [["A", "A"]]


def test_dependency_to_unknown_node_is_ignored():
    graph = {
        "A": ["B"],
    }

    detector = CircularDependencyDetector(graph)

    cycles = detector.detect()

    assert cycles == []


def test_duplicate_cycle_is_not_recorded():
    graph = {
        "A": ["B", "B"],
        "B": ["A"],
    }

    detector = CircularDependencyDetector(graph)

    cycles = detector.detect()

    assert cycles == [["A", "B", "A"]]


def test_empty_graph():
    graph = {}

    detector = CircularDependencyDetector(graph)

    cycles = detector.detect()

    assert cycles == []


def test_single_node_without_dependency():
    graph = {
        "A": [],
    }

    detector = CircularDependencyDetector(graph)

    cycles = detector.detect()

    assert cycles == []


def test_chain_without_cycle():
    graph = {
        "A": ["B"],
        "B": ["C"],
        "C": ["D"],
        "D": [],
    }

    detector = CircularDependencyDetector(graph)

    cycles = detector.detect()

    assert cycles == []