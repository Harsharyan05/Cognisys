"""
Symbol Semantic Search

Author: Harsh Aryan
Project: Cognisys
"""

from pathlib import Path

from sentence_transformers import SentenceTransformer

from app.ai.multi_vector_store import MultiVectorStore
from app.ai.symbol_embedding_indexer import SymbolEmbeddingIndexer


class SymbolSemanticSearch:
    """
    Performs semantic search over repository symbols.
    """

    def __init__(
        self,
        repository_path,
        vector_store_directory=None,
    ):

        self.repository_path = Path(repository_path)

        if not self.repository_path.exists():
            raise ValueError(
                "Repository path does not exist."
            )

        if not self.repository_path.is_dir():
            raise ValueError(
                "Repository path must be a directory."
            )

        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

        self.embedding_indexer = SymbolEmbeddingIndexer(
            repository_path=self.repository_path
        )

        if vector_store_directory is None:
            vector_store_directory = (
                Path("storage")
                / "repositories"
                / self.repository_path.name
                / "symbol_vector_db"
            )

        self.vector_store = MultiVectorStore(
            output_directory=str(
                vector_store_directory
            )
        )

        self._build_index()

    def _build_index(self):

        embeddings = (
            self.embedding_indexer.create_embeddings()
        )

        if not embeddings:
            return

        self.vector_store.build(
            embeddings
        )

    def search(
        self,
        query: str,
        top_k: int = 5,
    ):

        if not query or not query.strip():
            return []

        query_vector = self.model.encode(
            query,
            convert_to_numpy=True,
        )

        return self.vector_store.search(
            query_vector,
            k=top_k,
        )