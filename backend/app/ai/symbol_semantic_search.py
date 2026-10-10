
import hashlib
import json
from pathlib import Path

from sentence_transformers import SentenceTransformer

from app.ai.multi_vector_store import MultiVectorStore
from app.ai.symbol_embedding_indexer import SymbolEmbeddingIndexer


class SymbolSemanticSearch:
    """Semantic search over a cached repository symbol index."""

    MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

    IGNORED_DIRECTORIES = {
        ".git", ".venv", "venv", "__pycache__",
        "node_modules", ".pytest_cache", ".mypy_cache",
        ".ruff_cache", "storage",
    }

    def __init__(self, repository_path, vector_store_directory=None):
        self.repository_path = Path(repository_path).resolve()

        if not self.repository_path.is_dir():
            raise ValueError("Repository path must be an existing directory.")

        repository_key = hashlib.sha256(
            str(self.repository_path).encode("utf-8")
        ).hexdigest()[:16]

        if vector_store_directory is None:
            vector_store_directory = (
                Path("storage")
                / "repositories"
                / f"{self.repository_path.name}_{repository_key}"
                / "symbol_vector_db"
            )

        self.vector_store_directory = Path(vector_store_directory)
        self.vector_store_directory.mkdir(parents=True, exist_ok=True)
        self.state_path = self.vector_store_directory / "symbol_index_state.json"

        self.model = SentenceTransformer(self.MODEL_NAME)
        self.embedding_indexer = SymbolEmbeddingIndexer(
            repository_path=self.repository_path,
            model=self.model,
        )
        self.vector_store = MultiVectorStore(
            output_directory=str(self.vector_store_directory)
        )

        self._build_index()

    def _source_hashes(self):
        """Hash source files to detect additions, edits, and deletions."""
        hashes = {}

        for path in self.repository_path.rglob("*.py"):
            relative = path.relative_to(self.repository_path)

            if any(part in self.IGNORED_DIRECTORIES for part in relative.parts):
                continue

            try:
                digest = hashlib.sha256(path.read_bytes()).hexdigest()
            except OSError:
                continue

            hashes[relative.as_posix()] = digest

        return hashes

    def _cache_is_valid(self, current_hashes):
        index_path = self.vector_store_directory / "index.faiss"
        metadata_path = self.vector_store_directory / "metadata.pkl"

        if not index_path.is_file() or not metadata_path.is_file():
            return False

        try:
            with self.state_path.open("r", encoding="utf-8") as file:
                state = json.load(file)
            return state.get("files") == current_hashes
        except (OSError, ValueError, TypeError):
            return False

    def _build_index(self):
        current_hashes = self._source_hashes()

        if self._cache_is_valid(current_hashes):
            # Load the persisted FAISS index and its metadata.
            self.vector_store._load()
            return

        embeddings = self.embedding_indexer.create_embeddings()

        if embeddings:
            self.vector_store.build(embeddings)
        else:
            # Remove stale indexes if no symbols remain.
            for name in ("index.faiss", "metadata.pkl"):
                path = self.vector_store_directory / name
                if path.exists():
                    path.unlink()

        temporary_path = self.state_path.with_suffix(".tmp")
        with temporary_path.open("w", encoding="utf-8") as file:
            json.dump({"files": current_hashes}, file, indent=2)
        temporary_path.replace(self.state_path)

    def search(self, query: str, top_k: int = 5):
        if not query or not query.strip():
            return []

        index_path = self.vector_store_directory / "index.faiss"
        metadata_path = self.vector_store_directory / "metadata.pkl"

        if not index_path.is_file() or not metadata_path.is_file():
            return []

        query_vector = self.model.encode(
            query.strip(),
            convert_to_numpy=True,
        )

        return self.vector_store.search(query_vector, k=top_k)
