from unittest.mock import patch

from app.services.analysis_service import AnalysisService


@patch("app.services.analysis_service.ArchitectureEngine")
@patch("app.services.analysis_service.ArchitectureAnalyzer")
@patch("app.services.analysis_service.DependencyAnalyzer")
@patch("app.services.analysis_service.TechnologyDetector")
@patch("app.services.analysis_service.RepositoryScanner")
def test_analysis_service_runs_all_analyzers(
    mock_scanner,
    mock_technology,
    mock_dependency,
    mock_architecture_analyzer,
    mock_architecture_engine,
):
    mock_scanner.return_value.scan.return_value = {
        "repository_name": "demo"
    }

    mock_technology.return_value.detect.return_value = {
        "python": True
    }

    mock_dependency.return_value.analyze.return_value = {
        "dependencies": []
    }

    mock_architecture_analyzer.return_value.analyze.return_value = {
        "frontend": False,
        "backend": True,
        "architecture_type": "Backend",
    }

    mock_architecture_engine.return_value.analyze.return_value = {
        "layers": {},
        "dependency_graph": {},
        "cycles": [],
        "hotspots": [],
        "patterns": [],
        "recommendations": [],
    }

    result = AnalysisService.analyze("demo_repo")

    mock_scanner.return_value.scan.assert_called_once_with(
        "demo_repo"
    )

    mock_technology.return_value.detect.assert_called_once_with(
        "demo_repo"
    )

    mock_dependency.return_value.analyze.assert_called_once_with(
        "demo_repo"
    )

    mock_architecture_analyzer.return_value.analyze.assert_called_once_with(
        "demo_repo"
    )

    mock_architecture_engine.return_value.analyze.assert_called_once()

    assert result["repository"]["repository_name"] == "demo"
    assert result["technology"]["python"] is True
    assert result["dependencies"]["dependencies"] == []

    assert result["architecture"]["overview"]["backend"] is True
    assert result["architecture"]["intelligence"]["layers"] == {}


def test_analysis_service_passes_repository_path_to_architecture_engine():
    with patch(
        "app.services.analysis_service.RepositoryScanner"
    ) as scanner, patch(
        "app.services.analysis_service.TechnologyDetector"
    ) as technology, patch(
        "app.services.analysis_service.DependencyAnalyzer"
    ) as dependency, patch(
        "app.services.analysis_service.ArchitectureAnalyzer"
    ) as architecture_analyzer, patch(
        "app.services.analysis_service.ArchitectureEngine"
    ) as architecture_engine:

        scanner.return_value.scan.return_value = {}
        technology.return_value.detect.return_value = {}
        dependency.return_value.analyze.return_value = {}
        architecture_analyzer.return_value.analyze.return_value = {}

        architecture_engine.return_value.analyze.return_value = {
            "layers": {"Presentation": ["api"]},
            "dependency_graph": {},
            "cycles": [],
            "hotspots": [],
            "patterns": [],
            "recommendations": [],
        }

        AnalysisService.analyze("C:\\repo")

        architecture_engine.assert_called_once_with(
            "C:\\repo"
        )