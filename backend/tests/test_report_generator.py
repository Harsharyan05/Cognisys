import json

from app.architecture.hotspot_detector import Hotspot
from app.architecture.architecture_models import ArchitecturePattern
from app.architecture.recommendation_models import Recommendation
from app.architecture.report_generator import ReportGenerator


# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------

def create_hotspot(
    module="app.services.user_service",
    fan_in=8,
    fan_out=5,
    score=13,
    risk="HIGH",
):
    return Hotspot(
        module=module,
        fan_in=fan_in,
        fan_out=fan_out,
        score=score,
        risk=risk,
    )


def create_pattern(
    name="Layered Architecture",
    confidence=0.95,
    evidence=None,
):
    if evidence is None:
        evidence = [
            "Presentation layer detected",
            "Business layer detected",
            "Persistence layer detected",
        ]

    return ArchitecturePattern(
        name=name,
        confidence=confidence,
        evidence=evidence,
    )


def create_recommendation(
    priority="HIGH",
    title="High Coupling Detected",
    module="app.services.user_service",
    recommendation="Split this module into smaller services to reduce coupling.",
):
    return Recommendation(
        priority=priority,
        title=title,
        module=module,
        recommendation=recommendation,
    )


# ---------------------------------------------------------
# Initialization
# ---------------------------------------------------------

def test_report_generator_initialization(tmp_path):
    output_directory = tmp_path / "reports"

    generator = ReportGenerator(
        output_directory=str(output_directory)
    )

    assert generator.output_directory == output_directory
    assert output_directory.exists()
    assert output_directory.is_dir()


def test_report_generator_creates_nested_directory(tmp_path):
    output_directory = (
        tmp_path
        / "project"
        / "architecture"
        / "reports"
    )

    ReportGenerator(
        output_directory=str(output_directory)
    )

    assert output_directory.exists()
    assert output_directory.is_dir()


# ---------------------------------------------------------
# JSON Report
# ---------------------------------------------------------

def test_generate_json_creates_file(tmp_path):
    generator = ReportGenerator(
        output_directory=str(tmp_path)
    )

    output = generator.generate_json(
        hotspots=[],
        patterns=[],
        recommendations=[],
        cycles=[],
    )

    assert output.exists()
    assert output.is_file()
    assert output.name == "architecture_report.json"


def test_generate_json_returns_path(tmp_path):
    generator = ReportGenerator(
        output_directory=str(tmp_path)
    )

    output = generator.generate_json(
        hotspots=[],
        patterns=[],
        recommendations=[],
        cycles=[],
    )

    assert output == tmp_path / "architecture_report.json"


def test_generate_json_contains_expected_sections(tmp_path):
    generator = ReportGenerator(
        output_directory=str(tmp_path)
    )

    output = generator.generate_json(
        hotspots=[],
        patterns=[],
        recommendations=[],
        cycles=[],
    )

    with open(output, "r", encoding="utf-8") as file:
        report = json.load(file)

    assert "hotspots" in report
    assert "patterns" in report
    assert "recommendations" in report
    assert "cycles" in report


def test_generate_json_empty_inputs(tmp_path):
    generator = ReportGenerator(
        output_directory=str(tmp_path)
    )

    output = generator.generate_json(
        hotspots=[],
        patterns=[],
        recommendations=[],
        cycles=[],
    )

    with open(output, "r", encoding="utf-8") as file:
        report = json.load(file)

    assert report == {
        "hotspots": [],
        "patterns": [],
        "recommendations": [],
        "cycles": [],
    }


def test_generate_json_serializes_hotspots(tmp_path):
    hotspot = create_hotspot()

    generator = ReportGenerator(
        output_directory=str(tmp_path)
    )

    output = generator.generate_json(
        hotspots=[hotspot],
        patterns=[],
        recommendations=[],
        cycles=[],
    )

    with open(output, "r", encoding="utf-8") as file:
        report = json.load(file)

    assert len(report["hotspots"]) == 1

    assert report["hotspots"][0] == {
        "module": "app.services.user_service",
        "fan_in": 8,
        "fan_out": 5,
        "score": 13,
        "risk": "HIGH",
    }


def test_generate_json_serializes_patterns(tmp_path):
    pattern = create_pattern()

    generator = ReportGenerator(
        output_directory=str(tmp_path)
    )

    output = generator.generate_json(
        hotspots=[],
        patterns=[pattern],
        recommendations=[],
        cycles=[],
    )

    with open(output, "r", encoding="utf-8") as file:
        report = json.load(file)

    assert len(report["patterns"]) == 1

    assert report["patterns"][0]["name"] == "Layered Architecture"
    assert report["patterns"][0]["confidence"] == 0.95
    assert len(report["patterns"][0]["evidence"]) == 3


def test_generate_json_serializes_recommendations(tmp_path):
    recommendation = create_recommendation()

    generator = ReportGenerator(
        output_directory=str(tmp_path)
    )

    output = generator.generate_json(
        hotspots=[],
        patterns=[],
        recommendations=[recommendation],
        cycles=[],
    )

    with open(output, "r", encoding="utf-8") as file:
        report = json.load(file)

    assert len(report["recommendations"]) == 1

    assert report["recommendations"][0] == {
        "priority": "HIGH",
        "title": "High Coupling Detected",
        "module": "app.services.user_service",
        "recommendation": (
            "Split this module into smaller services "
            "to reduce coupling."
        ),
    }


def test_generate_json_serializes_cycles(tmp_path):
    cycles = [
        ["app.a", "app.b", "app.a"],
        ["app.x", "app.y", "app.x"],
    ]

    generator = ReportGenerator(
        output_directory=str(tmp_path)
    )

    output = generator.generate_json(
        hotspots=[],
        patterns=[],
        recommendations=[],
        cycles=cycles,
    )

    with open(output, "r", encoding="utf-8") as file:
        report = json.load(file)

    assert report["cycles"] == cycles


def test_generate_json_serializes_all_data(tmp_path):
    hotspot = create_hotspot()
    pattern = create_pattern()
    recommendation = create_recommendation()
    cycles = [["app.a", "app.b", "app.a"]]

    generator = ReportGenerator(
        output_directory=str(tmp_path)
    )

    output = generator.generate_json(
        hotspots=[hotspot],
        patterns=[pattern],
        recommendations=[recommendation],
        cycles=cycles,
    )

    with open(output, "r", encoding="utf-8") as file:
        report = json.load(file)

    assert len(report["hotspots"]) == 1
    assert len(report["patterns"]) == 1
    assert len(report["recommendations"]) == 1
    assert report["cycles"] == cycles


# ---------------------------------------------------------
# Markdown Report
# ---------------------------------------------------------

def test_generate_markdown_creates_file(tmp_path):
    generator = ReportGenerator(
        output_directory=str(tmp_path)
    )

    output = generator.generate_markdown(
        hotspots=[],
        patterns=[],
        recommendations=[],
        cycles=[],
    )

    assert output.exists()
    assert output.is_file()
    assert output.name == "architecture_report.md"


def test_generate_markdown_returns_path(tmp_path):
    generator = ReportGenerator(
        output_directory=str(tmp_path)
    )

    output = generator.generate_markdown(
        hotspots=[],
        patterns=[],
        recommendations=[],
        cycles=[],
    )

    assert output == tmp_path / "architecture_report.md"


def test_generate_markdown_contains_title(tmp_path):
    generator = ReportGenerator(
        output_directory=str(tmp_path)
    )

    output = generator.generate_markdown(
        hotspots=[],
        patterns=[],
        recommendations=[],
        cycles=[],
    )

    content = output.read_text(encoding="utf-8")

    assert content.startswith("# Cognisys Architecture Report")


def test_generate_markdown_contains_sections(tmp_path):
    generator = ReportGenerator(
        output_directory=str(tmp_path)
    )

    output = generator.generate_markdown(
        hotspots=[],
        patterns=[],
        recommendations=[],
        cycles=[],
    )

    content = output.read_text(encoding="utf-8")

    assert "## Architecture Patterns" in content
    assert "## Hotspots" in content
    assert "## Circular Dependencies" in content
    assert "## Recommendations" in content


def test_generate_markdown_contains_pattern_details(tmp_path):
    pattern = create_pattern()

    generator = ReportGenerator(
        output_directory=str(tmp_path)
    )

    output = generator.generate_markdown(
        hotspots=[],
        patterns=[pattern],
        recommendations=[],
        cycles=[],
    )

    content = output.read_text(encoding="utf-8")

    assert "### Layered Architecture" in content
    assert "- Confidence: 0.95" in content
    assert "- Evidence:" in content
    assert "- Presentation layer detected" in content
    assert "- Business layer detected" in content
    assert "- Persistence layer detected" in content


def test_generate_markdown_contains_hotspot_details(tmp_path):
    hotspot = create_hotspot()

    generator = ReportGenerator(
        output_directory=str(tmp_path)
    )

    output = generator.generate_markdown(
        hotspots=[hotspot],
        patterns=[],
        recommendations=[],
        cycles=[],
    )

    content = output.read_text(encoding="utf-8")

    assert "**app.services.user_service**" in content
    assert "Score: 13" in content
    assert "Risk: HIGH" in content


def test_generate_markdown_contains_cycle_details(tmp_path):
    cycles = [
        ["app.a", "app.b", "app.a"],
    ]

    generator = ReportGenerator(
        output_directory=str(tmp_path)
    )

    output = generator.generate_markdown(
        hotspots=[],
        patterns=[],
        recommendations=[],
        cycles=cycles,
    )

    content = output.read_text(encoding="utf-8")

    assert "app.a -> app.b -> app.a" in content


def test_generate_markdown_handles_no_cycles(tmp_path):
    generator = ReportGenerator(
        output_directory=str(tmp_path)
    )

    output = generator.generate_markdown(
        hotspots=[],
        patterns=[],
        recommendations=[],
        cycles=[],
    )

    content = output.read_text(encoding="utf-8")

    assert "No circular dependencies detected." in content


def test_generate_markdown_contains_recommendation_details(tmp_path):
    recommendation = create_recommendation()

    generator = ReportGenerator(
        output_directory=str(tmp_path)
    )

    output = generator.generate_markdown(
        hotspots=[],
        patterns=[],
        recommendations=[recommendation],
        cycles=[],
    )

    content = output.read_text(encoding="utf-8")

    assert "### High Coupling Detected" in content
    assert "- Priority: HIGH" in content
    assert "- Module: app.services.user_service" in content
    assert (
        "- Recommendation: Split this module into smaller services "
        "to reduce coupling."
    ) in content


def test_generate_markdown_contains_multiple_entries(tmp_path):
    hotspots = [
        create_hotspot(
            module="app.module_one",
            fan_in=8,
            fan_out=5,
            score=13,
            risk="HIGH",
        ),
        create_hotspot(
            module="app.module_two",
            fan_in=3,
            fan_out=3,
            score=6,
            risk="MEDIUM",
        ),
    ]

    patterns = [
        create_pattern(),
        create_pattern(
            name="MVC",
            confidence=0.60,
            evidence=[
                "Presentation layer detected",
                "Persistence layer detected",
            ],
        ),
    ]

    recommendations = [
        create_recommendation(),
        create_recommendation(
            priority="MEDIUM",
            title="Medium Coupling",
            module="app.module_two",
            recommendation=(
                "Consider refactoring this module "
                "if it continues to grow."
            ),
        ),
    ]

    cycles = [
        ["app.a", "app.b", "app.a"],
        ["app.x", "app.y", "app.x"],
    ]

    generator = ReportGenerator(
        output_directory=str(tmp_path)
    )

    output = generator.generate_markdown(
        hotspots=hotspots,
        patterns=patterns,
        recommendations=recommendations,
        cycles=cycles,
    )

    content = output.read_text(encoding="utf-8")

    assert "app.module_one" in content
    assert "app.module_two" in content
    assert "### Layered Architecture" in content
    assert "### MVC" in content
    assert "app.a -> app.b -> app.a" in content
    assert "app.x -> app.y -> app.x" in content
    assert "### High Coupling Detected" in content
    assert "### Medium Coupling" in content