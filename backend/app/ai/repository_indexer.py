
"""
Repository Indexer

Indexes a single repository into repository-specific storage
and reuses embeddings for unchanged files.

Author: Harsh Aryan
Project: Cognisys
"""

import hashlib
import json
import pickle
from pathlib import Path

from sentence_transformers import SentenceTransformer

from app.ai.embedding_models import Embedding
from app.ai.multi_vector_store import MultiVectorStore


class RepositoryIndexer:
    """
    Repository-specific indexing pipeline with incremental indexing.
    """

    MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

    IGNORED_DIRECTORIES = {
        ".git",
        ".venv",
        "venv",
        "__pycache__",
        "node_modules",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
    }

    def __init__(self, repository_path):
        self.repository_path = Path(repository_path).resolve()

        if not self.repository_path.exists():
            raise ValueError("Repository path does not exist.")

        if not self.repository_path.is_dir():
            raise ValueError("Repository path must be a directory.")

        self.repository_name = self.repository_path.name

        # Give each distinct repository path its own storage directory.
        repository_key = hashlib.sha256(
            str(self.repository_path).encode("utf-8")
        ).hexdigest()[:16]

        self.repository_storage = (
            Path("storage")
            / "repositories"
            / f"{self.repository_name}_{repository_key}"
        )

        self.vector_store_directory = (
            self.repository_storage / "vector_db"
        )

        self.state_path = (
            self.repository_storage / "index_state.json"
        )

        self.metadata_path = (
            self.vector_store_directory / "metadata.pkl"
        )

    @staticmethod
    def _file_hash(file_path):
        """Calculate a SHA-256 hash without loading the whole file."""

        digest = hashlib.sha256()

        with Path(file_path).open("rb") as file:
            for block in iter(
                lambda: file.read(1024 * 1024),
                b"",
            ):
                digest.update(block)

        return digest.hexdigest()

    def discover_files(self):
        """
        Discover repository files while excluding common generated directories.
        """

        files = []

        for path in self.repository_path.rglob("*"):
            if not path.is_file():
                continue

            relative_parts = path.relative_to(
                self.repository_path
            ).parts

            if any(
                part in self.IGNORED_DIRECTORIES
                for part in relative_parts
            ):
                continue

            # Do not index this indexer's own generated storage.
            if "storage" in relative_parts:
                continue

            files.append(path)

        return sorted(files)

    def create_documents(self):
        """
        Convert readable repository files into documents with hashes.
        """

        documents = []

        for file_path in self.discover_files():
            try:
                content = file_path.read_text(
                    encoding="utf-8"
                )
                file_hash = self._file_hash(file_path)

            except (UnicodeDecodeError, OSError):
                continue

            relative_path = file_path.relative_to(
                self.repository_path
            ).as_posix()

            documents.append(
                {
                    "content": content,
                    "metadata": {
                        "source": relative_path,
                        "repository": self.repository_name,
                        "file_hash": file_hash,
                    },
                }
            )

        return documents

    def create_chunks(self):
        """
        Create one chunk per file, preserving source and hash metadata.
        """

        chunks = []

        for index, document in enumerate(
            self.create_documents(),
            start=1,
        ):
            chunks.append(
                {
                    "content": document["content"],
                    "metadata": {
                        "chunk_id": index,
                        **document["metadata"],
                    },
                }
            )

        return chunks

    def create_embeddings(self, chunks):
        """
        Generate embeddings for the supplied chunks.
        """

        if not chunks:
            return []

        model = SentenceTransformer(self.MODEL_NAME)
        embeddings = []

        for chunk in chunks:
            text = chunk["content"]
            metadata = chunk["metadata"]
            source = metadata["source"]

            vector = model.encode(
                text,
                convert_to_numpy=True,
            )

            embedding = Embedding(
                chunk_id=metadata["chunk_id"],
                title=Path(source).name,
                source_document=source,
                text=text,
                word_count=len(text.split()),
                vector=vector,
                dimension=len(vector),
                metadata={
                    "repository": metadata["repository"],
                    "source": source,
                    "file_hash": metadata["file_hash"],
                },
            )

            embeddings.append(embedding)

        return embeddings

    def _load_previous_data(self):
        """
        Load previously saved embeddings and file hashes.

        If the cache is absent or incompatible, return empty data so
        the next indexing operation performs a full index.
        """

        if (
            not self.metadata_path.exists()
            or not self.state_path.exists()
        ):
            return {}, {}

        try:
            with self.metadata_path.open("rb") as file:
                embeddings = pickle.load(file)

            with self.state_path.open(
                "r",
                encoding="utf-8",
            ) as file:
                state = json.load(file)

            if not isinstance(embeddings, list):
                return {}, {}

            previous_embeddings = {}

            for embedding in embeddings:
                source = getattr(
                    embedding,
                    "source_document",
                    None,
                )

                if not source:
                    continue

                previous_embeddings[source] = embedding

            previous_hashes = state.get("files", {})

            if not isinstance(previous_hashes, dict):
                return {}, {}

            return previous_embeddings, previous_hashes

        except (
            OSError,
            EOFError,
            pickle.PickleError,
            ValueError,
            TypeError,
            AttributeError,
        ):
            return {}, {}

    def _save_index_state(self, file_hashes):
        """Persist hashes for the current readable repository files."""

        self.repository_storage.mkdir(
            parents=True,
            exist_ok=True,
        )

        temporary_path = self.state_path.with_suffix(
            ".json.tmp"
        )

        with temporary_path.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                {
                    "repository": self.repository_name,
                    "repository_path": str(self.repository_path),
                    "files": file_hashes,
                },
                file,
                indent=2,
            )

        temporary_path.replace(self.state_path)

    def index(self):
        """
        Incrementally index a repository.

        Unchanged files reuse their previous embeddings.
        Added or modified files receive new embeddings.
        Deleted or unreadable files are excluded from the new index.
        """

        self.repository_storage.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.vector_store_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        chunks = self.create_chunks()

        current_hashes = {
            chunk["metadata"]["source"]:
                chunk["metadata"]["file_hash"]
            for chunk in chunks
        }

        previous_embeddings, previous_hashes = (
            self._load_previous_data()
        )

        unchanged_embeddings = []
        changed_chunks = []

        for chunk in chunks:
            metadata = chunk["metadata"]
            source = metadata["source"]
            file_hash = metadata["file_hash"]

            cached_embedding = previous_embeddings.get(source)

            cache_is_valid = (
                cached_embedding is not None
                and previous_hashes.get(source) == file_hash
                and getattr(
                    cached_embedding,
                    "metadata",
                    {},
                ).get("file_hash") == file_hash
            )

            if cache_is_valid:
                unchanged_embeddings.append(cached_embedding)
            else:
                changed_chunks.append(chunk)

        deleted_files = (
            set(previous_hashes) - set(current_hashes)
        )

        # Embed only new or modified files.
        new_embeddings = (
            self.create_embeddings(changed_chunks)
            if changed_chunks
            else []
        )
            
        embeddings = unchanged_embeddings + new_embeddings

        if not embeddings:
            # Remove stale indexes when no readable files remain.
            for filename in ("index.faiss", "metadata.pkl"):
                stale_file = self.vector_store_directory / filename

                if stale_file.exists():
                    stale_file.unlink()

            self._save_index_state(current_hashes)

            return {
                "repository": self.repository_name,
                "chunks": 0,
                "embeddings": 0,
                "unchanged_files": 0,
                "changed_or_added_files": 0,
                "deleted_files": len(deleted_files),
                "vector_store": str(self.vector_store_directory),
            }

        # Rebuild the vector store from all current embeddings.
        # This also removes vectors for deleted files.
        vector_store = MultiVectorStore(
            output_directory=str(self.vector_store_directory)
        )

        vector_store.build(embeddings)

        self._save_index_state(current_hashes)

        return {
            "repository": self.repository_name,
            "chunks": len(embeddings),
            "embeddings": len(embeddings),
            "unchanged_files": len(unchanged_embeddings),
            "changed_or_added_files": len(changed_chunks),
            "deleted_files": len(deleted_files),
            "vector_store": str(self.vector_store_directory),
        }
