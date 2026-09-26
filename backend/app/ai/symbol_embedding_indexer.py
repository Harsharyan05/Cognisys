"""
Symbol Embedding Indexer

Author: Harsh Aryan
Project: Cognisys
"""

from pathlib import Path

from sentence_transformers import SentenceTransformer

from app.ai.embedding_models import Embedding
from app.ai.symbol_indexer import SymbolIndexer


class SymbolEmbeddingIndexer:
    """
    Converts symbol-level chunks into Embedding objects.
    """

    def __init__(self, repository_path):

        self.repository_path = Path(repository_path)

        if not self.repository_path.exists():
            raise ValueError(
                "Repository path does not exist."
            )

        if not self.repository_path.is_dir():
            raise ValueError(
                "Repository path must be a directory."
            )

        self.symbol_indexer = SymbolIndexer(
            repository_path=self.repository_path
        )

        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

    def create_embeddings(self):

        chunks = self.symbol_indexer.create_symbol_chunks()

        embeddings = []

        for index, chunk in enumerate(
            chunks,
            start=1,
        ):

            text = chunk["content"]

            vector = self.model.encode(
                text,
                convert_to_numpy=True,
            )

            metadata = chunk["metadata"]

            embedding = Embedding(
                chunk_id=index,
                title=metadata["symbol_name"],
                source_document=metadata["source"],
                text=text,
                word_count=len(text.split()),
                vector=vector,
                dimension=len(vector),
                line_start=metadata["line"],
                line_end=metadata["line_end"],
                metadata=metadata,
            )

            embeddings.append(embedding)

        return embeddings