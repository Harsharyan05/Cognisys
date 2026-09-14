from app.architecture.hotspot_detector import (
    Hotspot,
    HotspotDetector,
)


def test_hotspot_dataclass():
    hotspot = Hotspot(
        module="app.main",
        fan_in=3,
        fan_out=2,
        score=5,
        risk="MEDIUM",
    )

    assert hotspot.module == "app.main"
    assert hotspot.fan_in == 3
    assert hotspot.fan_out == 2
    assert hotspot.score == 5
    assert hotspot.risk == "MEDIUM"


def test_initialization():
    graph = {
        "A": ["B"],
        "B": [],
    }

    detector = HotspotDetector(graph)

    assert detector.graph == graph


def test_empty_graph():
    detector = HotspotDetector({})

    hotspots = detector.detect()

    assert hotspots == []


def test_no_dependencies():
    graph = {
        "A": [],
        "B": [],
    }

    detector = HotspotDetector(graph)

    hotspots = detector.detect()

    assert len(hotspots) == 2

    for hotspot in hotspots:
        assert hotspot.fan_in == 0
        assert hotspot.fan_out == 0
        assert hotspot.score == 0
        assert hotspot.risk == "LOW"


def test_fan_out():
    graph = {
        "A": ["B", "C", "D"],
        "B": [],
        "C": [],
        "D": [],
    }

    detector = HotspotDetector(graph)

    hotspots = detector.detect()

    hotspot_a = next(
        hotspot
        for hotspot in hotspots
        if hotspot.module == "A"
    )

    assert hotspot_a.fan_out == 3
    assert hotspot_a.fan_in == 0
    assert hotspot_a.score == 3
    assert hotspot_a.risk == "LOW"


def test_fan_in():
    graph = {
        "A": [],
        "B": ["A"],
        "C": ["A"],
        "D": ["A"],
    }

    detector = HotspotDetector(graph)

    hotspots = detector.detect()

    hotspot_a = next(
        hotspot
        for hotspot in hotspots
        if hotspot.module == "A"
    )

    assert hotspot_a.fan_in == 3
    assert hotspot_a.fan_out == 0
    assert hotspot_a.score == 3
    assert hotspot_a.risk == "LOW"


def test_score_is_fan_in_plus_fan_out():
    graph = {
        "A": ["B", "C"],
        "B": ["A"],
        "C": [],
    }

    detector = HotspotDetector(graph)

    hotspots = detector.detect()

    hotspot_a = next(
        hotspot
        for hotspot in hotspots
        if hotspot.module == "A"
    )

    assert hotspot_a.fan_in == 1
    assert hotspot_a.fan_out == 2
    assert hotspot_a.score == 3


def test_low_risk():
    detector = HotspotDetector({})

    assert detector._calculate_risk(0) == "LOW"
    assert detector._calculate_risk(1) == "LOW"
    assert detector._calculate_risk(4) == "LOW"


def test_medium_risk():
    detector = HotspotDetector({})

    assert detector._calculate_risk(5) == "MEDIUM"
    assert detector._calculate_risk(6) == "MEDIUM"
    assert detector._calculate_risk(9) == "MEDIUM"


def test_high_risk():
    detector = HotspotDetector({})

    assert detector._calculate_risk(10) == "HIGH"
    assert detector._calculate_risk(15) == "HIGH"
    assert detector._calculate_risk(100) == "HIGH"


def test_risk_boundaries():
    detector = HotspotDetector({})

    assert detector._calculate_risk(4) == "LOW"
    assert detector._calculate_risk(5) == "MEDIUM"
    assert detector._calculate_risk(9) == "MEDIUM"
    assert detector._calculate_risk(10) == "HIGH"


def test_high_fan_in_creates_high_risk():
    graph = {
        "A": [],
        "B": ["A"],
        "C": ["A"],
        "D": ["A"],
        "E": ["A"],
        "F": ["A"],
        "G": ["A"],
        "H": ["A"],
        "I": ["A"],
        "J": ["A"],
        "K": ["A"],
    }

    detector = HotspotDetector(graph)

    hotspots = detector.detect()

    hotspot_a = next(
        hotspot
        for hotspot in hotspots
        if hotspot.module == "A"
    )

    assert hotspot_a.fan_in == 10
    assert hotspot_a.fan_out == 0
    assert hotspot_a.score == 10
    assert hotspot_a.risk == "HIGH"


def test_init_modules_are_ignored():
    graph = {
        "app.__init__": ["A"],
        "A": ["B"],
        "B": [],
    }

    detector = HotspotDetector(graph)

    hotspots = detector.detect()

    modules = [
        hotspot.module
        for hotspot in hotspots
    ]

    assert "app.__init__" not in modules
    assert "A" in modules
    assert "B" in modules


def test_init_dependencies_are_ignored():
    graph = {
        "A": ["B", "app.__init__"],
        "B": [],
        "app.__init__": [],
    }

    detector = HotspotDetector(graph)

    hotspots = detector.detect()

    hotspot_a = next(
        hotspot
        for hotspot in hotspots
        if hotspot.module == "A"
    )

    assert hotspot_a.fan_out == 1
    assert hotspot_a.score == 1


def test_results_sorted_by_score():
    graph = {
        "A": ["B", "C", "D"],
        "B": ["A", "C"],
        "C": ["A"],
        "D": [],
    }

    detector = HotspotDetector(graph)

    hotspots = detector.detect()

    scores = [
        hotspot.score
        for hotspot in hotspots
    ]

    assert scores == sorted(
        scores,
        reverse=True,
    )


def test_multiple_hotspots():
    graph = {
        "A": ["B", "C"],
        "B": ["A"],
        "C": ["A"],
        "D": ["A", "B"],
    }

    detector = HotspotDetector(graph)

    hotspots = detector.detect()

    assert len(hotspots) == 4

    for hotspot in hotspots:
        assert hotspot.score == (
            hotspot.fan_in + hotspot.fan_out
        )

        assert hotspot.risk in {
            "LOW",
            "MEDIUM",
            "HIGH",
        }