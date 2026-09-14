from pathlib import Path
from unittest.mock import patch

from app.architecture.architecture_engine import ArchitectureEngine
from app.architecture.hotspot_detector import Hotspot
from app.architecture.architecture_models import ArchitecturePattern
from app.architecture.recommendation_models import Recommendation


# ---------------------------------------------------------
# Fixtures / Sample Data
# ---------------------------------------------------------

def sample_layers():
    return {
        "Presentation": ["app/api"],
        "Business": ["app/services"],
        "Persistence": ["app/database"],
    }


def sample_dependency_graph():
    return {
        "app.main": ["app.api"],
        "app.api": ["app.services"],
        "app.services": ["app.database"],
    }


def sample_cycles():
    return [
        ["app.a", "app.b", "app.a"],
    ]


def sample_hotspots():
    return [
        Hotspot(
            module="app.services",
            fan_in=5,
            fan_out=3,
            score=8,
            risk="MEDIUM",
        )
    ]


def sample_patterns():
    return [
        ArchitecturePattern(
            name="Layered Architecture",
            confidence=0.95,
            evidence=[
                "Business layer detected",
                "Persistence layer detected",
                "Presentation layer detected",
            ],
        )
    ]


def sample_recommendations():
    return [
        Recommendation(
            priority="MEDIUM",
            title="Medium Coupling",
            module="app.services",
            recommendation=(
                "Consider refactoring this module "
                "if it continues to grow."
            ),
        )
    ]


# ---------------------------------------------------------
# Initialization
# ---------------------------------------------------------

def test_engine_initialization():
    engine = ArchitectureEngine(
        repository_path=".",
        output_directory="reports",
    )

    assert engine.repository_path == Path(".")
    assert engine.output_directory == "reports"


def test_engine_accepts_custom_repository_path():
    engine = ArchitectureEngine(
        repository_path="my_repository",
        output_directory="my_reports",
    )

    assert engine.repository_path == Path("my_repository")
    assert engine.output_directory == "my_reports"


# ---------------------------------------------------------
# Layer Detection
# ---------------------------------------------------------

@patch("app.architecture.architecture_engine.LayerDetector")
@patch("app.architecture.architecture_engine.DependencyGraph")
@patch("app.architecture.architecture_engine.CircularDependencyDetector")
@patch("app.architecture.architecture_engine.HotspotDetector")
@patch("app.architecture.architecture_engine.ArchitecturePatternDetector")
@patch("app.architecture.architecture_engine.RecommendationEngine")
@patch("app.architecture.architecture_engine.ReportGenerator")
def test_analyze_calls_layer_detector(
    mock_report_generator,
    mock_recommendation_engine,
    mock_pattern_detector,
    mock_hotspot_detector,
    mock_cycle_detector,
    mock_dependency_graph,
    mock_layer_detector,
):
    mock_layer_detector.return_value.detect.return_value = sample_layers()

    mock_dependency_graph.return_value.build.return_value = {}
    mock_cycle_detector.return_value.detect.return_value = []
    mock_hotspot_detector.return_value.detect.return_value = []
    mock_pattern_detector.return_value.detect.return_value = []
    mock_recommendation_engine.return_value.generate.return_value = []

    mock_report_generator.return_value.generate_json.return_value = Path(
        "reports/architecture_report.json"
    )

    mock_report_generator.return_value.generate_markdown.return_value = Path(
        "reports/architecture_report.md"
    )

    engine = ArchitectureEngine("repository")

    engine.analyze()

    mock_layer_detector.assert_called_once_with("repository")


# ---------------------------------------------------------
# Dependency Graph
# ---------------------------------------------------------

@patch("app.architecture.architecture_engine.LayerDetector")
@patch("app.architecture.architecture_engine.DependencyGraph")
@patch("app.architecture.architecture_engine.CircularDependencyDetector")
@patch("app.architecture.architecture_engine.HotspotDetector")
@patch("app.architecture.architecture_engine.ArchitecturePatternDetector")
@patch("app.architecture.architecture_engine.RecommendationEngine")
@patch("app.architecture.architecture_engine.ReportGenerator")
def test_analyze_calls_dependency_graph(
    mock_report_generator,
    mock_recommendation_engine,
    mock_pattern_detector,
    mock_hotspot_detector,
    mock_cycle_detector,
    mock_dependency_graph,
    mock_layer_detector,
):
    graph = sample_dependency_graph()

    mock_layer_detector.return_value.detect.return_value = {}
    mock_dependency_graph.return_value.build.return_value = graph
    mock_cycle_detector.return_value.detect.return_value = []
    mock_hotspot_detector.return_value.detect.return_value = []
    mock_pattern_detector.return_value.detect.return_value = []
    mock_recommendation_engine.return_value.generate.return_value = []

    mock_report_generator.return_value.generate_json.return_value = Path(
        "architecture_report.json"
    )
    mock_report_generator.return_value.generate_markdown.return_value = Path(
        "architecture_report.md"
    )

    engine = ArchitectureEngine("repository")

    engine.analyze()

    mock_dependency_graph.assert_called_once_with("repository")
    mock_dependency_graph.return_value.build.assert_called_once()


# ---------------------------------------------------------
# Circular Dependency Detector
# ---------------------------------------------------------

@patch("app.architecture.architecture_engine.LayerDetector")
@patch("app.architecture.architecture_engine.DependencyGraph")
@patch("app.architecture.architecture_engine.CircularDependencyDetector")
@patch("app.architecture.architecture_engine.HotspotDetector")
@patch("app.architecture.architecture_engine.ArchitecturePatternDetector")
@patch("app.architecture.architecture_engine.RecommendationEngine")
@patch("app.architecture.architecture_engine.ReportGenerator")
def test_analyze_passes_graph_to_cycle_detector(
    mock_report_generator,
    mock_recommendation_engine,
    mock_pattern_detector,
    mock_hotspot_detector,
    mock_cycle_detector,
    mock_dependency_graph,
    mock_layer_detector,
):
    graph = sample_dependency_graph()

    mock_layer_detector.return_value.detect.return_value = {}
    mock_dependency_graph.return_value.build.return_value = graph
    mock_cycle_detector.return_value.detect.return_value = []
    mock_hotspot_detector.return_value.detect.return_value = []
    mock_pattern_detector.return_value.detect.return_value = []
    mock_recommendation_engine.return_value.generate.return_value = []

    mock_report_generator.return_value.generate_json.return_value = Path(
        "architecture_report.json"
    )
    mock_report_generator.return_value.generate_markdown.return_value = Path(
        "architecture_report.md"
    )

    engine = ArchitectureEngine("repository")

    engine.analyze()

    mock_cycle_detector.assert_called_once_with(graph)
    mock_cycle_detector.return_value.detect.assert_called_once()


# ---------------------------------------------------------
# Hotspot Detector
# ---------------------------------------------------------

@patch("app.architecture.architecture_engine.LayerDetector")
@patch("app.architecture.architecture_engine.DependencyGraph")
@patch("app.architecture.architecture_engine.CircularDependencyDetector")
@patch("app.architecture.architecture_engine.HotspotDetector")
@patch("app.architecture.architecture_engine.ArchitecturePatternDetector")
@patch("app.architecture.architecture_engine.RecommendationEngine")
@patch("app.architecture.architecture_engine.ReportGenerator")
def test_analyze_passes_graph_to_hotspot_detector(
    mock_report_generator,
    mock_recommendation_engine,
    mock_pattern_detector,
    mock_hotspot_detector,
    mock_cycle_detector,
    mock_dependency_graph,
    mock_layer_detector,
):
    graph = sample_dependency_graph()

    mock_layer_detector.return_value.detect.return_value = {}
    mock_dependency_graph.return_value.build.return_value = graph
    mock_cycle_detector.return_value.detect.return_value = []
    mock_hotspot_detector.return_value.detect.return_value = []
    mock_pattern_detector.return_value.detect.return_value = []
    mock_recommendation_engine.return_value.generate.return_value = []

    mock_report_generator.return_value.generate_json.return_value = Path(
        "architecture_report.json"
    )
    mock_report_generator.return_value.generate_markdown.return_value = Path(
        "architecture_report.md"
    )

    engine = ArchitectureEngine("repository")

    engine.analyze()

    mock_hotspot_detector.assert_called_once_with(graph)
    mock_hotspot_detector.return_value.detect.assert_called_once()


# ---------------------------------------------------------
# Architecture Pattern Detector
# ---------------------------------------------------------

@patch("app.architecture.architecture_engine.LayerDetector")
@patch("app.architecture.architecture_engine.DependencyGraph")
@patch("app.architecture.architecture_engine.CircularDependencyDetector")
@patch("app.architecture.architecture_engine.HotspotDetector")
@patch("app.architecture.architecture_engine.ArchitecturePatternDetector")
@patch("app.architecture.architecture_engine.RecommendationEngine")
@patch("app.architecture.architecture_engine.ReportGenerator")
def test_analyze_passes_layers_and_graph_to_pattern_detector(
    mock_report_generator,
    mock_recommendation_engine,
    mock_pattern_detector,
    mock_hotspot_detector,
    mock_cycle_detector,
    mock_dependency_graph,
    mock_layer_detector,
):
    layers = sample_layers()
    graph = sample_dependency_graph()

    mock_layer_detector.return_value.detect.return_value = layers
    mock_dependency_graph.return_value.build.return_value = graph
    mock_cycle_detector.return_value.detect.return_value = []
    mock_hotspot_detector.return_value.detect.return_value = []
    mock_pattern_detector.return_value.detect.return_value = []
    mock_recommendation_engine.return_value.generate.return_value = []

    mock_report_generator.return_value.generate_json.return_value = Path(
        "architecture_report.json"
    )
    mock_report_generator.return_value.generate_markdown.return_value = Path(
        "architecture_report.md"
    )

    engine = ArchitectureEngine("repository")

    engine.analyze()

    mock_pattern_detector.assert_called_once_with(
        layers,
        graph,
    )

    mock_pattern_detector.return_value.detect.assert_called_once()


# ---------------------------------------------------------
# Recommendation Engine
# ---------------------------------------------------------

@patch("app.architecture.architecture_engine.LayerDetector")
@patch("app.architecture.architecture_engine.DependencyGraph")
@patch("app.architecture.architecture_engine.CircularDependencyDetector")
@patch("app.architecture.architecture_engine.HotspotDetector")
@patch("app.architecture.architecture_engine.ArchitecturePatternDetector")
@patch("app.architecture.architecture_engine.RecommendationEngine")
@patch("app.architecture.architecture_engine.ReportGenerator")
def test_analyze_passes_analysis_results_to_recommendation_engine(
    mock_report_generator,
    mock_recommendation_engine,
    mock_pattern_detector,
    mock_hotspot_detector,
    mock_cycle_detector,
    mock_dependency_graph,
    mock_layer_detector,
):
    cycles = sample_cycles()
    hotspots = sample_hotspots()
    patterns = sample_patterns()

    mock_layer_detector.return_value.detect.return_value = {}
    mock_dependency_graph.return_value.build.return_value = {}
    mock_cycle_detector.return_value.detect.return_value = cycles
    mock_hotspot_detector.return_value.detect.return_value = hotspots
    mock_pattern_detector.return_value.detect.return_value = patterns
    mock_recommendation_engine.return_value.generate.return_value = []

    mock_report_generator.return_value.generate_json.return_value = Path(
        "architecture_report.json"
    )
    mock_report_generator.return_value.generate_markdown.return_value = Path(
        "architecture_report.md"
    )

    engine = ArchitectureEngine("repository")

    engine.analyze()

    mock_recommendation_engine.assert_called_once_with(
        hotspots,
        cycles,
        patterns,
    )

    mock_recommendation_engine.return_value.generate.assert_called_once()


# ---------------------------------------------------------
# Report Generator
# ---------------------------------------------------------

@patch("app.architecture.architecture_engine.LayerDetector")
@patch("app.architecture.architecture_engine.DependencyGraph")
@patch("app.architecture.architecture_engine.CircularDependencyDetector")
@patch("app.architecture.architecture_engine.HotspotDetector")
@patch("app.architecture.architecture_engine.ArchitecturePatternDetector")
@patch("app.architecture.architecture_engine.RecommendationEngine")
@patch("app.architecture.architecture_engine.ReportGenerator")
def test_analyze_creates_report_generator(
    mock_report_generator,
    mock_recommendation_engine,
    mock_pattern_detector,
    mock_hotspot_detector,
    mock_cycle_detector,
    mock_dependency_graph,
    mock_layer_detector,
):
    mock_layer_detector.return_value.detect.return_value = {}
    mock_dependency_graph.return_value.build.return_value = {}
    mock_cycle_detector.return_value.detect.return_value = []
    mock_hotspot_detector.return_value.detect.return_value = []
    mock_pattern_detector.return_value.detect.return_value = []
    mock_recommendation_engine.return_value.generate.return_value = []

    mock_report_generator.return_value.generate_json.return_value = Path(
        "architecture_report.json"
    )
    mock_report_generator.return_value.generate_markdown.return_value = Path(
        "architecture_report.md"
    )

    engine = ArchitectureEngine(
        "repository",
        output_directory="custom_reports",
    )

    engine.analyze()

    mock_report_generator.assert_called_once_with(
        "custom_reports"
    )


@patch("app.architecture.architecture_engine.LayerDetector")
@patch("app.architecture.architecture_engine.DependencyGraph")
@patch("app.architecture.architecture_engine.CircularDependencyDetector")
@patch("app.architecture.architecture_engine.HotspotDetector")
@patch("app.architecture.architecture_engine.ArchitecturePatternDetector")
@patch("app.architecture.architecture_engine.RecommendationEngine")
@patch("app.architecture.architecture_engine.ReportGenerator")
def test_analyze_generates_json_report(
    mock_report_generator,
    mock_recommendation_engine,
    mock_pattern_detector,
    mock_hotspot_detector,
    mock_cycle_detector,
    mock_dependency_graph,
    mock_layer_detector,
):
    layers = sample_layers()
    graph = sample_dependency_graph()
    cycles = sample_cycles()
    hotspots = sample_hotspots()
    patterns = sample_patterns()
    recommendations = sample_recommendations()

    mock_layer_detector.return_value.detect.return_value = layers
    mock_dependency_graph.return_value.build.return_value = graph
    mock_cycle_detector.return_value.detect.return_value = cycles
    mock_hotspot_detector.return_value.detect.return_value = hotspots
    mock_pattern_detector.return_value.detect.return_value = patterns
    mock_recommendation_engine.return_value.generate.return_value = recommendations

    json_report = Path("custom/architecture_report.json")
    markdown_report = Path("custom/architecture_report.md")

    mock_report_generator.return_value.generate_json.return_value = json_report
    mock_report_generator.return_value.generate_markdown.return_value = markdown_report

    engine = ArchitectureEngine("repository")

    result = engine.analyze()

    mock_report_generator.return_value.generate_json.assert_called_once_with(
        hotspots,
        patterns,
        recommendations,
        cycles,
    )

    assert result["json_report"] == json_report


@patch("app.architecture.architecture_engine.LayerDetector")
@patch("app.architecture.architecture_engine.DependencyGraph")
@patch("app.architecture.architecture_engine.CircularDependencyDetector")
@patch("app.architecture.architecture_engine.HotspotDetector")
@patch("app.architecture.architecture_engine.ArchitecturePatternDetector")
@patch("app.architecture.architecture_engine.RecommendationEngine")
@patch("app.architecture.architecture_engine.ReportGenerator")
def test_analyze_generates_markdown_report(
    mock_report_generator,
    mock_recommendation_engine,
    mock_pattern_detector,
    mock_hotspot_detector,
    mock_cycle_detector,
    mock_dependency_graph,
    mock_layer_detector,
):
    layers = sample_layers()
    graph = sample_dependency_graph()
    cycles = sample_cycles()
    hotspots = sample_hotspots()
    patterns = sample_patterns()
    recommendations = sample_recommendations()

    mock_layer_detector.return_value.detect.return_value = layers
    mock_dependency_graph.return_value.build.return_value = graph
    mock_cycle_detector.return_value.detect.return_value = cycles
    mock_hotspot_detector.return_value.detect.return_value = hotspots
    mock_pattern_detector.return_value.detect.return_value = patterns
    mock_recommendation_engine.return_value.generate.return_value = recommendations

    json_report = Path("architecture_report.json")
    markdown_report = Path("architecture_report.md")

    mock_report_generator.return_value.generate_json.return_value = json_report
    mock_report_generator.return_value.generate_markdown.return_value = markdown_report

    engine = ArchitectureEngine("repository")

    result = engine.analyze()

    mock_report_generator.return_value.generate_markdown.assert_called_once_with(
        hotspots,
        patterns,
        recommendations,
        cycles,
    )

    assert result["markdown_report"] == markdown_report


# ---------------------------------------------------------
# Return Structure
# ---------------------------------------------------------

@patch("app.architecture.architecture_engine.LayerDetector")
@patch("app.architecture.architecture_engine.DependencyGraph")
@patch("app.architecture.architecture_engine.CircularDependencyDetector")
@patch("app.architecture.architecture_engine.HotspotDetector")
@patch("app.architecture.architecture_engine.ArchitecturePatternDetector")
@patch("app.architecture.architecture_engine.RecommendationEngine")
@patch("app.architecture.architecture_engine.ReportGenerator")
def test_analyze_returns_all_expected_keys(
    mock_report_generator,
    mock_recommendation_engine,
    mock_pattern_detector,
    mock_hotspot_detector,
    mock_cycle_detector,
    mock_dependency_graph,
    mock_layer_detector,
):
    layers = sample_layers()
    graph = sample_dependency_graph()
    cycles = sample_cycles()
    hotspots = sample_hotspots()
    patterns = sample_patterns()
    recommendations = sample_recommendations()

    json_report = Path("architecture_report.json")
    markdown_report = Path("architecture_report.md")

    mock_layer_detector.return_value.detect.return_value = layers
    mock_dependency_graph.return_value.build.return_value = graph
    mock_cycle_detector.return_value.detect.return_value = cycles
    mock_hotspot_detector.return_value.detect.return_value = hotspots
    mock_pattern_detector.return_value.detect.return_value = patterns
    mock_recommendation_engine.return_value.generate.return_value = recommendations

    mock_report_generator.return_value.generate_json.return_value = json_report
    mock_report_generator.return_value.generate_markdown.return_value = markdown_report

    engine = ArchitectureEngine("repository")

    result = engine.analyze()

    expected_keys = {
        "layers",
        "dependency_graph",
        "cycles",
        "hotspots",
        "patterns",
        "recommendations",
        "json_report",
        "markdown_report",
    }

    assert set(result.keys()) == expected_keys


@patch("app.architecture.architecture_engine.LayerDetector")
@patch("app.architecture.architecture_engine.DependencyGraph")
@patch("app.architecture.architecture_engine.CircularDependencyDetector")
@patch("app.architecture.architecture_engine.HotspotDetector")
@patch("app.architecture.architecture_engine.ArchitecturePatternDetector")
@patch("app.architecture.architecture_engine.RecommendationEngine")
@patch("app.architecture.architecture_engine.ReportGenerator")
def test_analyze_returns_correct_analysis_results(
    mock_report_generator,
    mock_recommendation_engine,
    mock_pattern_detector,
    mock_hotspot_detector,
    mock_cycle_detector,
    mock_dependency_graph,
    mock_layer_detector,
):
    layers = sample_layers()
    graph = sample_dependency_graph()
    cycles = sample_cycles()
    hotspots = sample_hotspots()
    patterns = sample_patterns()
    recommendations = sample_recommendations()

    json_report = Path("architecture_report.json")
    markdown_report = Path("architecture_report.md")

    mock_layer_detector.return_value.detect.return_value = layers
    mock_dependency_graph.return_value.build.return_value = graph
    mock_cycle_detector.return_value.detect.return_value = cycles
    mock_hotspot_detector.return_value.detect.return_value = hotspots
    mock_pattern_detector.return_value.detect.return_value = patterns
    mock_recommendation_engine.return_value.generate.return_value = recommendations

    mock_report_generator.return_value.generate_json.return_value = json_report
    mock_report_generator.return_value.generate_markdown.return_value = markdown_report

    engine = ArchitectureEngine("repository")

    result = engine.analyze()

    assert result["layers"] == layers
    assert result["dependency_graph"] == graph
    assert result["cycles"] == cycles
    assert result["hotspots"] == hotspots
    assert result["patterns"] == patterns
    assert result["recommendations"] == recommendations
    assert result["json_report"] == json_report
    assert result["markdown_report"] == markdown_report


# ---------------------------------------------------------
# Empty Analysis
# ---------------------------------------------------------

@patch("app.architecture.architecture_engine.LayerDetector")
@patch("app.architecture.architecture_engine.DependencyGraph")
@patch("app.architecture.architecture_engine.CircularDependencyDetector")
@patch("app.architecture.architecture_engine.HotspotDetector")
@patch("app.architecture.architecture_engine.ArchitecturePatternDetector")
@patch("app.architecture.architecture_engine.RecommendationEngine")
@patch("app.architecture.architecture_engine.ReportGenerator")
def test_analyze_handles_empty_analysis(
    mock_report_generator,
    mock_recommendation_engine,
    mock_pattern_detector,
    mock_hotspot_detector,
    mock_cycle_detector,
    mock_dependency_graph,
    mock_layer_detector,
):
    mock_layer_detector.return_value.detect.return_value = {}
    mock_dependency_graph.return_value.build.return_value = {}
    mock_cycle_detector.return_value.detect.return_value = []
    mock_hotspot_detector.return_value.detect.return_value = []
    mock_pattern_detector.return_value.detect.return_value = []
    mock_recommendation_engine.return_value.generate.return_value = []

    mock_report_generator.return_value.generate_json.return_value = Path(
        "architecture_report.json"
    )
    mock_report_generator.return_value.generate_markdown.return_value = Path(
        "architecture_report.md"
    )

    engine = ArchitectureEngine("repository")

    result = engine.analyze()

    assert result["layers"] == {}
    assert result["dependency_graph"] == {}
    assert result["cycles"] == []
    assert result["hotspots"] == []
    assert result["patterns"] == []
    assert result["recommendations"] == []