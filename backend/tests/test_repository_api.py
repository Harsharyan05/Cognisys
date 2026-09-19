from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_clone_repository_endpoint():
    with patch(
        "app.api.v1.repository.RepositoryService.clone_repository"
    ) as clone_mock:

        clone_mock.return_value = {
            "status": "success",
            "repository_name": "cognisys",
            "local_path": "storage/temp/cognisys",
        }

        response = client.post(
            "/api/v1/repositories/clone",
            json={
                "repository_url": (
                    "https://github.com/example/cognisys.git"
                )
            },
        )

        assert response.status_code == 200

        assert response.json() == {
            "status": "success",
            "repository_name": "cognisys",
            "local_path": "storage/temp/cognisys",
        }

        clone_mock.assert_called_once_with(
            "https://github.com/example/cognisys.git"
        )


def test_clone_repository_invalid_url():
    response = client.post(
        "/api/v1/repositories/clone",
        json={
            "repository_url": "not-a-valid-url"
        },
    )

    assert response.status_code == 422


def test_clone_repository_service_error():
    with patch(
        "app.api.v1.repository.RepositoryService.clone_repository"
    ) as clone_mock:

        clone_mock.side_effect = ValueError(
            "Failed to clone repository."
        )

        response = client.post(
            "/api/v1/repositories/clone",
            json={
                "repository_url": (
                    "https://github.com/example/missing.git"
                )
            },
        )

        assert response.status_code == 400
        assert response.json()["detail"] == (
            "Failed to clone repository."
        )