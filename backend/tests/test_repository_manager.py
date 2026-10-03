"""
Tests for RepositoryManager.

Author: Harsh Aryan
Project: Cognisys
"""

from datetime import datetime

import pytest

from app.repository.repository_manager import RepositoryManager


@pytest.fixture
def manager(tmp_path):
    return RepositoryManager(storage_directory=tmp_path)


def test_register_repository(manager, tmp_path):
    metadata = manager.register_repository(
        repository_url="https://github.com/example/demo",
        repository_name="demo",
        owner="example",
        local_path=str(tmp_path / "demo"),
        commit_sha="abc123",
    )

    assert metadata["repository_url"] == (
        "https://github.com/example/demo"
    )
    assert metadata["repository_name"] == "demo"
    assert metadata["owner"] == "example"
    assert metadata["local_path"] == str(tmp_path / "demo")
    assert metadata["commit_sha"] == "abc123"
    assert metadata["status"] == "registered"
    assert metadata["repository_id"]


def test_register_repository_creates_persistent_metadata(
    manager,
    tmp_path,
):
    manager.register_repository(
        repository_url="https://github.com/example/demo",
        repository_name="demo",
        owner="example",
        local_path=str(tmp_path / "demo"),
        commit_sha="abc123",
    )

    assert manager.repository_exists("example/demo")

    stored = manager.get_repository("example/demo")

    assert stored is not None
    assert stored["repository_name"] == "demo"


def test_repository_exists_returns_false_for_unknown_repository(
    manager,
):
    assert manager.repository_exists("example/unknown") is False


def test_get_repository_returns_none_for_unknown_repository(
    manager,
):
    assert manager.get_repository("example/unknown") is None


def test_get_repository_returns_registered_repository(
    manager,
    tmp_path,
):
    manager.register_repository(
        repository_url="https://github.com/example/demo",
        repository_name="demo",
        owner="example",
        local_path=str(tmp_path / "demo"),
        commit_sha="abc123",
    )

    repository = manager.get_repository("example/demo")

    assert repository["owner"] == "example"
    assert repository["repository_name"] == "demo"
    assert repository["commit_sha"] == "abc123"


def test_update_repository(manager, tmp_path):
    manager.register_repository(
        repository_url="https://github.com/example/demo",
        repository_name="demo",
        owner="example",
        local_path=str(tmp_path / "demo"),
        commit_sha="abc123",
    )

    updated = manager.update_repository(
        "example/demo",
        commit_sha="def456",
        status="indexed",
    )

    assert updated["commit_sha"] == "def456"
    assert updated["status"] == "indexed"


def test_update_repository_persists_changes(
    manager,
    tmp_path,
):
    manager.register_repository(
        repository_url="https://github.com/example/demo",
        repository_name="demo",
        owner="example",
        local_path=str(tmp_path / "demo"),
        commit_sha="abc123",
    )

    manager.update_repository(
        "example/demo",
        status="indexed",
    )

    repository = manager.get_repository("example/demo")

    assert repository["status"] == "indexed"


def test_update_unknown_repository_raises_error(manager):
    with pytest.raises(KeyError):
        manager.update_repository(
            "example/unknown",
            status="indexed",
        )

    # ========================================================
    # LIST
    # ========================================================

    def list_repositories(self):
        repositories = []

        if not self.storage_directory.exists():
            return repositories

        for repository_directory in self.storage_directory.iterdir():
            if not repository_directory.is_dir():
                continue

            metadata_path = (
                repository_directory
                / "metadata.json"
            )

            if not metadata_path.exists():
                continue

            try:
                metadata = self._read_metadata(
                    metadata_path
                )
            except (OSError, json.JSONDecodeError):
                continue

            repositories.append(metadata)

        return repositories

def test_delete_repository(manager, tmp_path):
    manager.register_repository(
        repository_url="https://github.com/example/demo",
        repository_name="demo",
        owner="example",
        local_path=str(tmp_path / "demo"),
        commit_sha="abc123",
    )

    result = manager.delete_repository("example/demo")

    assert result is True
    assert manager.repository_exists("example/demo") is False


def test_delete_unknown_repository_returns_false(manager):
    result = manager.delete_repository("example/unknown")

    assert result is False


def test_repository_has_indexed_at_timestamp(
    manager,
    tmp_path,
):
    metadata = manager.register_repository(
        repository_url="https://github.com/example/demo",
        repository_name="demo",
        owner="example",
        local_path=str(tmp_path / "demo"),
        commit_sha="abc123",
    )

    assert metadata["indexed_at"] is None


def test_repository_has_created_at_timestamp(
    manager,
    tmp_path,
):
    metadata = manager.register_repository(
        repository_url="https://github.com/example/demo",
        repository_name="demo",
        owner="example",
        local_path=str(tmp_path / "demo"),
        commit_sha="abc123",
    )

    assert metadata["created_at"]

    datetime.fromisoformat(
        metadata["created_at"]
    )


def test_update_repository_updates_timestamp(
    manager,
    tmp_path,
):
    manager.register_repository(
        repository_url="https://github.com/example/demo",
        repository_name="demo",
        owner="example",
        local_path=str(tmp_path / "demo"),
        commit_sha="abc123",
    )

    updated = manager.update_repository(
        "example/demo",
        status="indexed",
    )

    assert updated["updated_at"]

    datetime.fromisoformat(
        updated["updated_at"]
    )
    
def test_register_existing_repository_updates_metadata(
    manager,
    tmp_path,
):
    first = manager.register_repository(
        repository_url="https://github.com/example/demo",
        repository_name="demo",
        owner="example",
        local_path=str(tmp_path / "demo"),
        commit_sha="abc123",
    )

    second = manager.register_repository(
        repository_url="https://github.com/example/demo",
        repository_name="demo",
        owner="example",
        local_path=str(tmp_path / "demo"),
        commit_sha="def456",
    )

    assert second["repository_id"] == first["repository_id"]
    assert second["commit_sha"] == "def456"

    stored = manager.get_repository("example/demo")

    assert stored["commit_sha"] == "def456"  
    
def test_list_repositories(manager, tmp_path):
    manager.register_repository(
        repository_url="https://github.com/example/repo-a",
        repository_name="repo-a",
        owner="example",
        local_path=str(tmp_path / "repo-a"),
        commit_sha="abc123",
    )

    manager.register_repository(
        repository_url="https://github.com/example/repo-b",
        repository_name="repo-b",
        owner="example",
        local_path=str(tmp_path / "repo-b"),
        commit_sha="def456",
    )

    repositories = manager.list_repositories()

    assert len(repositories) == 2

    repository_ids = {
        repository["repository_id"]
        for repository in repositories
    }

    assert "example/repo-a" in repository_ids
    assert "example/repo-b" in repository_ids  
    
def test_repository_status_can_be_updated(manager, tmp_path):
    manager.register_repository(
        repository_url="https://github.com/example/demo",
        repository_name="demo",
        owner="example",
        local_path=str(tmp_path / "demo"),
    )

    updated = manager.update_repository(
        "example/demo",
        status="indexing",
    )

    assert updated["status"] == "indexing"

    stored = manager.get_repository("example/demo")

    assert stored["status"] == "indexing"


def test_repository_can_be_marked_indexed(manager, tmp_path):
    manager.register_repository(
        repository_url="https://github.com/example/demo",
        repository_name="demo",
        owner="example",
        local_path=str(tmp_path / "demo"),
    )

    updated = manager.update_repository(
        "example/demo",
        status="indexed",
        indexed_at="2026-10-04T00:00:00+00:00",
    )

    assert updated["status"] == "indexed"
    assert updated["indexed_at"] == "2026-10-04T00:00:00+00:00"


def test_repository_can_be_marked_failed(manager, tmp_path):
    manager.register_repository(
        repository_url="https://github.com/example/demo",
        repository_name="demo",
        owner="example",
        local_path=str(tmp_path / "demo"),
    )

    updated = manager.update_repository(
        "example/demo",
        status="failed",
    )

    assert updated["status"] == "failed"      
    
def test_mark_indexing(manager, tmp_path):
    manager.register_repository(
        repository_url="https://github.com/example/demo",
        repository_name="demo",
        owner="example",
        local_path=str(tmp_path / "demo"),
    )

    updated = manager.mark_indexing("example/demo")

    assert updated["status"] == "indexing"


def test_mark_indexed(manager, tmp_path):
    manager.register_repository(
        repository_url="https://github.com/example/demo",
        repository_name="demo",
        owner="example",
        local_path=str(tmp_path / "demo"),
    )

    updated = manager.mark_indexed(
        "example/demo",
        commit_sha="abc123",
    )

    assert updated["status"] == "indexed"
    assert updated["commit_sha"] == "abc123"
    assert updated["indexed_at"] is not None


def test_mark_failed(manager, tmp_path):
    manager.register_repository(
        repository_url="https://github.com/example/demo",
        repository_name="demo",
        owner="example",
        local_path=str(tmp_path / "demo"),
    )

    updated = manager.mark_failed(
        "example/demo"
    )

    assert updated["status"] == "failed"          