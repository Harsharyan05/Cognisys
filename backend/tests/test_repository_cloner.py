from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from app.parser.repository_cloner import RepositoryCloner


def test_clone_returns_repository_name_and_path():
    with patch(
        "app.parser.repository_cloner.Repo.clone_from"
    ) as clone_mock, patch(
        "app.parser.repository_cloner.TEMP_DIR",
        Path("test_storage"),
    ):

        repository_name, local_path = RepositoryCloner.clone(
            "https://github.com/example/cognisys.git"
        )

        assert repository_name == "cognisys"
        assert local_path.endswith(
            "test_storage\\cognisys"
        )

        clone_mock.assert_called_once()


def test_clone_uses_cached_repository():
    with patch(
        "app.parser.repository_cloner.TEMP_DIR",
        Path("test_storage"),
    ):

        destination = Path("test_storage") / "cognisys"
        destination.mkdir(
            parents=True,
            exist_ok=True,
        )

        with patch(
            "app.parser.repository_cloner.Repo.clone_from"
        ) as clone_mock:

            repository_name, local_path = (
                RepositoryCloner.clone(
                    "https://github.com/example/cognisys.git"
                )
            )

            assert repository_name == "cognisys"
            assert local_path.endswith(
                "test_storage\\cognisys"
            )

            clone_mock.assert_not_called()

        destination.rmdir()


def test_clone_raises_value_error_on_git_failure():
    from git import GitCommandError

    with patch(
        "app.parser.repository_cloner.TEMP_DIR",
        Path("test_storage"),
    ), patch(
        "app.parser.repository_cloner.Repo.clone_from",
        side_effect=GitCommandError(
            "clone",
            "repository not found",
        ),
    ):

        with pytest.raises(ValueError) as error:
            RepositoryCloner.clone(
                "https://github.com/example/missing.git"
            )

        assert str(error.value) == (
            "Failed to clone repository."
        )
