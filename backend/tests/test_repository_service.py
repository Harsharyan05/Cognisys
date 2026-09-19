from unittest.mock import patch

from app.services.repository_service import RepositoryService


def test_clone_repository_delegates_to_cloner():
    with patch(
        "app.services.repository_service.RepositoryCloner.clone"
    ) as clone_mock:

        clone_mock.return_value = (
            "cognisys",
            "storage/temp/cognisys",
        )

        result = RepositoryService.clone_repository(
            "https://github.com/example/cognisys.git"
        )

        clone_mock.assert_called_once_with(
            "https://github.com/example/cognisys.git"
        )

        assert result == {
            "status": "success",
            "repository_name": "cognisys",
            "local_path": "storage/temp/cognisys",
        }


def test_clone_repository_propagates_clone_error():
    with patch(
        "app.services.repository_service.RepositoryCloner.clone"
    ) as clone_mock:

        clone_mock.side_effect = ValueError(
            "Failed to clone repository."
        )

        try:
            RepositoryService.clone_repository(
                "https://github.com/example/missing.git"
            )
            assert False, "Expected ValueError"
        except ValueError as error:
            assert str(error) == (
                "Failed to clone repository."
            )
