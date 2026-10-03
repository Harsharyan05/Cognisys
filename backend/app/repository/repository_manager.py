"""
Repository persistence manager.

Author: Harsh Aryan
Project: Cognisys
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4


class RepositoryManager:
    """
    Manages persistent repository metadata for Cognisys.
    """

    def __init__(self, storage_directory="storage/repositories"):
        self.storage_directory = Path(storage_directory)
        self.storage_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    # ========================================================
    # REGISTER
    # ========================================================

    def register_repository(
        self,
        repository_url,
        repository_name,
        owner,
        local_path,
        commit_sha=None,
    ):
        repository_id = f"{owner}/{repository_name}"

        now = datetime.now(
            timezone.utc
        ).isoformat()

        metadata = {
            "repository_id": repository_id,
            "repository_url": repository_url,
            "repository_name": repository_name,
            "owner": owner,
            "local_path": local_path,
            "commit_sha": commit_sha,
            "status": "registered",
            "created_at": now,
            "updated_at": now,
            "indexed_at": None,
        }

        repository_directory = (
            self.storage_directory
            / self._safe_repository_name(repository_id)
        )

        repository_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        metadata_path = (
            repository_directory
            / "metadata.json"
        )

        self._write_metadata(
            metadata_path,
            metadata,
        )

        return metadata

    # ========================================================
    # GET
    # ========================================================

    def get_repository(self, repository_id):
        metadata_path = self._metadata_path(
            repository_id
        )

        if not metadata_path.exists():
            return None

        return self._read_metadata(metadata_path)

    # ========================================================
    # EXISTS
    # ========================================================

    def repository_exists(self, repository_id):
        return (
            self._metadata_path(repository_id).exists()
        )

    # ========================================================
    # UPDATE
    # ========================================================

    def update_repository(
        self,
        repository_id,
        **updates,
    ):
        metadata_path = self._metadata_path(
            repository_id
        )

        if not metadata_path.exists():
            raise KeyError(
                f"Repository not found: {repository_id}"
            )

        metadata = self._read_metadata(
            metadata_path
        )

        allowed_fields = {
            "repository_url",
            "repository_name",
            "owner",
            "local_path",
            "commit_sha",
            "status",
            "indexed_at",
        }

        for key, value in updates.items():
            if key in allowed_fields:
                metadata[key] = value

        metadata["updated_at"] = (
            datetime.now(
                timezone.utc
            ).isoformat()
        )

        self._write_metadata(
            metadata_path,
            metadata,
        )

        return metadata
    
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

    # ========================================================
    # STATUS HELPERS
    # ========================================================

    def mark_indexing(self, repository_id):
        return self.update_repository(
            repository_id,
            status="indexing",
        )

    def mark_indexed(self, repository_id, commit_sha=None):
        indexed_at = datetime.now(
            timezone.utc
        ).isoformat()

        updates = {
            "status": "indexed",
            "indexed_at": indexed_at,
        }

        if commit_sha is not None:
            updates["commit_sha"] = commit_sha

        return self.update_repository(
            repository_id,
            **updates,
        )

    def mark_failed(self, repository_id):
        return self.update_repository(
            repository_id,
            status="failed",
        )
        
    # ========================================================
    # DELETE
    # ========================================================

    def delete_repository(self, repository_id):
        repository_directory = (
            self.storage_directory
            / self._safe_repository_name(
                repository_id
            )
        )

        metadata_path = (
            repository_directory
            / "metadata.json"
        )

        if not metadata_path.exists():
            return False

        metadata_path.unlink()

        try:
            repository_directory.rmdir()
        except OSError:
            pass

        return True

    # ========================================================
    # INTERNAL HELPERS
    # ========================================================

    def _metadata_path(self, repository_id):
        return (
            self.storage_directory
            / self._safe_repository_name(
                repository_id
            )
            / "metadata.json"
        )

    def _safe_repository_name(self, repository_id):
        return (
            repository_id
            .replace("/", "__")
            .replace("\\", "__")
            .replace(":", "_")
        )

    def _write_metadata(
        self,
        metadata_path,
        metadata,
    ):
        with metadata_path.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                metadata,
                file,
                indent=2,
            )

    def _read_metadata(self, metadata_path):
        with metadata_path.open(
            "r",
            encoding="utf-8",
        ) as file:
            return json.load(file)