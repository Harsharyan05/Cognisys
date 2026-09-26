"""
Hybrid Retriever

Author: Harsh Aryan
Project: Cognisys
"""

import re
from pathlib import Path
from typing import List

from app.ai.symbol_semantic_search import SymbolSemanticSearch
from app.ai.multi_semantic_search import MultiSemanticSearch
from app.ai.query_classifier import QueryClassifier
from app.ai.embedding_models import Embedding


class HybridRetriever:
    """
    Hybrid Retrieval Engine.

    Combines:
    - File-level Semantic Search
    - Symbol-level Semantic Search
    - Keyword Matching
    - Document Priority
    - Hybrid Scoring
    - Duplicate Removal
    - Re-ranking
    - Adaptive Top-K Retrieval
    """

    DOCUMENT_PRIORITY = {
        "repository_summary.md": 10,
        "architecture.md": 9,
        "services.md": 8,
        "apis.md": 8,
        "dependency_graph.md": 7,
        "technologies.md": 7,
        "architecture_patterns.md": 6,
        "hotspots.md": 5,
        "recommendations.md": 4,
    }

    STOP_WORDS = {
        "a",
        "an",
        "and",
        "are",
        "as",
        "at",
        "be",
        "by",
        "for",
        "from",
        "how",
        "in",
        "is",
        "it",
        "of",
        "on",
        "or",
        "that",
        "the",
        "this",
        "to",
        "what",
        "where",
        "which",
        "who",
        "with",
    }

    def __init__(
        self,
        vector_store_directory: str = "storage/vector_db",
        repository_path=None,
    ):
        self.repository_path = (
            Path(repository_path)
            if repository_path is not None
            else None
        )

        # -----------------------------------------------------
        # File-level semantic search
        # -----------------------------------------------------

        self.semantic_search = MultiSemanticSearch(
            vector_store_directory=vector_store_directory
        )

        self.classifier = QueryClassifier()

        self.document_priority = (
            self.DOCUMENT_PRIORITY.copy()
        )

        # -----------------------------------------------------
        # Symbol-level semantic search
        # -----------------------------------------------------

        self.symbol_search = None

        if self.repository_path is not None:

            self.symbol_search = SymbolSemanticSearch(
                repository_path=self.repository_path
            )

    # ---------------------------------------------------------
    # Query Tokenization
    # ---------------------------------------------------------

    def _extract_keywords(
        self,
        query: str,
    ) -> List[str]:

        words = re.findall(
            r"[a-zA-Z0-9_\-\.]+",
            query.lower(),
        )

        keywords = [
            word
            for word in words
            if word not in self.STOP_WORDS
            and len(word) > 1
        ]

        return keywords

    # ---------------------------------------------------------
    # Keyword Search
    # ---------------------------------------------------------

    def keyword_search(
        self,
        query: str,
        semantic_results,
    ):
        """
        Calculate keyword relevance for semantic results.
        """

        words = self._extract_keywords(query)

        results = []

        for embedding, distance in semantic_results:

            keyword_score = 0

            title = (
                embedding.title or ""
            ).lower()

            source_document = (
                embedding.source_document or ""
            ).lower()

            content = (
                embedding.text or ""
            ).lower()

            for word in words:

                if word in title:
                    keyword_score += 3

                if word in source_document:
                    keyword_score += 2

                if word in content:
                    keyword_score += 1

            results.append(
                (
                    embedding,
                    distance,
                    keyword_score,
                )
            )

        return results

    # ---------------------------------------------------------
    # Semantic Score
    # ---------------------------------------------------------

    @staticmethod
    def _semantic_score(
        distance: float,
    ) -> float:

        if distance < 0:
            distance = 0

        return 1.0 / (
            1.0 + distance
        )

    # ---------------------------------------------------------
    # Document Priority
    # ---------------------------------------------------------

    def _document_priority(
        self,
        embedding: Embedding,
    ) -> int:

        source_document = (
            embedding.source_document or ""
        )

        filename = (
            source_document
            .replace("\\", "/")
            .split("/")[-1]
        )

        return self.document_priority.get(
            filename,
            1,
        )

    # ---------------------------------------------------------
    # Symbol Priority
    # ---------------------------------------------------------

    @staticmethod
    def _symbol_priority(
        embedding: Embedding,
    ) -> int:
        """
        Give symbol-level results a small retrieval
        boost without destroying file-level ranking.
        """

        metadata = getattr(
            embedding,
            "metadata",
            {},
        ) or {}

        symbol_type = metadata.get(
            "symbol_type"
        )

        if symbol_type == "method":
            return 3

        if symbol_type == "function":
            return 3

        if symbol_type == "class":
            return 2

        return 0

    # ---------------------------------------------------------
    # Final Hybrid Score
    # ---------------------------------------------------------

    def calculate_score(
        self,
        embedding: Embedding,
        distance: float,
        keyword_score: int,
    ) -> float:

        semantic_score = (
            self._semantic_score(
                distance
            )
        )

        priority = (
            self._document_priority(
                embedding
            )
        )

        symbol_priority = (
            self._symbol_priority(
                embedding
            )
        )

        final_score = (
            semantic_score * 10.0
            + keyword_score * 2.0
            + priority
            + symbol_priority
        )

        return float(
            final_score
        )

    # ---------------------------------------------------------
    # Re-ranking
    # ---------------------------------------------------------

    def rerank(
        self,
        results,
    ):
        """
        Re-rank results using the hybrid score.
        """

        ranked = []

        for (
            embedding,
            distance,
            keyword_score,
        ) in results:

            score = self.calculate_score(
                embedding=embedding,
                distance=distance,
                keyword_score=keyword_score,
            )

            ranked.append(
                (
                    score,
                    embedding,
                    distance,
                )
            )

        ranked.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        return ranked

    # ---------------------------------------------------------
    # Duplicate Removal
    # ---------------------------------------------------------

    def remove_duplicates(
        self,
        ranked_results,
    ):
        """
        Remove duplicate repository chunks.

        Symbol results are identified by symbol_id.
        File results are identified by source + chunk_id.
        """

        unique = []

        seen = set()

        for (
            score,
            embedding,
            distance,
        ) in ranked_results:

            metadata = getattr(
                embedding,
                "metadata",
                {},
            ) or {}

            symbol_id = metadata.get(
                "symbol_id"
            )

            if symbol_id:

                key = (
                    "symbol",
                    symbol_id,
                )

            else:

                key = (
                    "file",
                    embedding.source_document,
                    embedding.chunk_id,
                )

            if key in seen:
                continue

            seen.add(key)

            unique.append(
                (
                    score,
                    embedding,
                    distance,
                )
            )

        return unique

    # ---------------------------------------------------------
    # Symbol Retrieval
    # ---------------------------------------------------------

    def _retrieve_symbols(
        self,
        question: str,
        candidate_k: int,
    ):
        """
        Retrieve symbol-level results.

        Symbol retrieval is optional. If it fails,
        file-level retrieval continues normally.
        """

        if self.symbol_search is None:
            return []

        try:

            return self.symbol_search.search(
                query=question,
                top_k=candidate_k,
            )

        except Exception:

            return []

    # ---------------------------------------------------------
    # Convert Symbol Results
    # ---------------------------------------------------------

    def _prepare_symbol_results(
        self,
        question: str,
        symbol_results,
    ):
        """
        Convert symbol search results into the same
        structure expected by the existing hybrid
        scoring pipeline.
        """

        if not symbol_results:
            return []

        words = self._extract_keywords(
            question
        )

        prepared = []

        for (
            embedding,
            distance,
        ) in symbol_results:

            keyword_score = 0

            title = (
                embedding.title or ""
            ).lower()

            source_document = (
                embedding.source_document or ""
            ).lower()

            content = (
                embedding.text or ""
            ).lower()

            metadata = getattr(
                embedding,
                "metadata",
                {},
            ) or {}

            symbol_name = (
                metadata.get(
                    "symbol_name",
                    "",
                )
                or ""
            ).lower()

            for word in words:

                if word in symbol_name:
                    keyword_score += 4

                if word in title:
                    keyword_score += 3

                if word in source_document:
                    keyword_score += 2

                if word in content:
                    keyword_score += 1

            prepared.append(
                (
                    embedding,
                    distance,
                    keyword_score,
                )
            )

        return prepared

    # ---------------------------------------------------------
    # Retrieval
    # ---------------------------------------------------------

    def retrieve(
        self,
        question: str,
        top_k: int | None = None,
    ):
        """
        Retrieve the most relevant repository context.

        Pipeline:

        Question
            ↓
        Query Classification
            ↓
        File Semantic Retrieval
            +
        Symbol Semantic Retrieval
            ↓
        Keyword Scoring
            ↓
        Hybrid Re-ranking
            ↓
        Duplicate Removal
            ↓
        Top-K Results
        """

        if not question:
            return []

        question = question.strip()

        if not question:
            return []

        # -----------------------------------------------------
        # Query Classification
        # -----------------------------------------------------

        classification = (
            self.classifier.classify(
                question
            )
        )

        # -----------------------------------------------------
        # Determine final Top-K
        # -----------------------------------------------------

        final_top_k = (
            top_k
            if top_k is not None
            else classification.top_k
        )

        # -----------------------------------------------------
        # Retrieve more candidates
        # -----------------------------------------------------

        candidate_k = max(
            final_top_k * 2,
            15,
        )

        # -----------------------------------------------------
        # File-Level Semantic Search
        # -----------------------------------------------------

        try:

            semantic_results = (
                self.semantic_search.search(
                    query=question,
                    top_k=candidate_k,
                )
            )

        except (
            FileNotFoundError,
            RuntimeError,
            OSError,
        ):

            semantic_results = []

        # -----------------------------------------------------
        # File-Level Keyword Scoring
        # -----------------------------------------------------

        file_keyword_results = []

        if semantic_results:

            file_keyword_results = (
                self.keyword_search(
                    query=question,
                    semantic_results=semantic_results,
                )
            )

        # -----------------------------------------------------
        # Symbol-Level Semantic Search
        # -----------------------------------------------------

        symbol_results = (
            self._retrieve_symbols(
                question=question,
                candidate_k=candidate_k,
            )
        )

        symbol_keyword_results = (
            self._prepare_symbol_results(
                question=question,
                symbol_results=symbol_results,
            )
        )

        # -----------------------------------------------------
        # Combine File + Symbol Results
        # -----------------------------------------------------

        combined_results = (
            file_keyword_results
            + symbol_keyword_results
        )

        if not combined_results:
            return []

        # -----------------------------------------------------
        # Hybrid Re-ranking
        # -----------------------------------------------------

        ranked_results = (
            self.rerank(
                combined_results
            )
        )

        # -----------------------------------------------------
        # Duplicate Removal
        # -----------------------------------------------------

        unique_results = (
            self.remove_duplicates(
                ranked_results
            )
        )

        # -----------------------------------------------------
        # Return Top Results
        # -----------------------------------------------------

        return unique_results[
            :final_top_k
        ]