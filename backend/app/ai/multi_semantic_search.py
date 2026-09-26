"""
Multi Semantic Search

Semantic search over repository knowledge.

Author: Harsh Aryan
Project: Cognisys
"""

from typing import List

from sentence_transformers import SentenceTransformer

from app.ai.embedding_models import Embedding
from app.ai.multi_vector_store import MultiVectorStore


class MultiSemanticSearch:
    """
    Performs semantic search over the repository.
    """

    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
        vector_store_directory: str = "storage/vector_db",
    ):

        print("Loading embedding model...")

        self.model = SentenceTransformer(model_name)

        print("Embedding model loaded.")

        self.vector_store = MultiVectorStore(
            output_directory=vector_store_directory
        )
        
    def search(
        self,
        query: str,
        top_k: int = 15,
    ) -> List[Embedding]:

        query_vector = self.model.encode(
            query,
            convert_to_numpy=True,
        )

        results = self.vector_store.search(
            query_vector=query_vector,
            k=top_k,
        )

        return results