from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


@patch("app.api.v1.analysis.AnalysisService.analyze")
@patch("app.api.v1.analysis.RepositoryService.clone_repository")
def test_analyze_repository_success(
    mock_clone,
    mock_analyze,
):
    mock_clone.return_value = {
        "status": "success",
        "repository_name": "demo",
        "local_path": "C:\\repo\\demo",
    }

    mock_analyze.return_value = {
        "repository": {
            "repository_name": "demo",
        },
        "technology": {
            "python": True,
        },
        "dependencies": {},
        "architecture": {
            "overview": {},
            "intelligence": {},
        },
    }

    response = client.post(
        "/api/v1/analysis/analyze",
        json={
            "repository_url": "https://github.com/example/demo"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"
    assert data["repository"]["repository_name"] == "demo"
    assert data["technology"]["python"] is True

    mock_clone.assert_called_once_with(
        "https://github.com/example/demo"
    )

    mock_analyze.assert_called_once_with(
        "C:\\repo\\demo"
    )


def test_analyze_repository_invalid_url():
    response = client.post(
        "/api/v1/analysis/analyze",
        json={
            "repository_url": "not-a-valid-url"
        },
    )

    assert response.status_code == 422