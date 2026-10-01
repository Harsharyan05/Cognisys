from app.ai.architecture_citation_engine import (
    ArchitectureCitationEngine,
)
from app.intelligence.architecture_context import (
    ArchitectureContext,
)
from app.intelligence.architecture_aware_retriever import (
    ArchitectureAwareRetriever,
)
from app.intelligence.query_classifier import (
    IntelligenceQueryClassifier,
)
from app.intelligence.unified_context import (
    UnifiedContext,
)


class IntelligenceEngine:
    """
    High-level orchestrator for Cognisys repository intelligence.

    Routes questions to:
    - RAG
    - Architecture
    - Both
    - Impact analysis
    - Graph-aware queries

    UnifiedContext combines the intelligence sources.
    """

    def __init__(
        self,
        rag_pipeline,
        architecture_engine,
        impact_engine=None,
        code_graph_engine=None,
        graph_aware_query=None,
    ):
        self.rag_pipeline = rag_pipeline
        self.architecture_engine = architecture_engine
        self.impact_engine = impact_engine
        self.code_graph_engine = code_graph_engine
        self.graph_aware_query = graph_aware_query

        self.query_classifier = (
            IntelligenceQueryClassifier()
        )

    def ask(self, question: str):
        classification = (
            self.query_classifier.classify(
                question
            )
        )

        # =====================================================
        # RAG
        # =====================================================

        if classification.category == "RAG":
            result = self.rag_pipeline.ask(
                question
            )

            return {
                "category": "RAG",
                **result,
            }

        # =====================================================
        # ARCHITECTURE
        # =====================================================

        if classification.category == "ARCHITECTURE":
            architecture_analysis = (
                self.architecture_engine.analyze()
            )

            architecture_context = (
                ArchitectureContext(
                    architecture_analysis
                )
            )

            architecture_retriever = (
                ArchitectureAwareRetriever(
                    architecture_analysis
                )
            )

            architecture_retrieval = (
                architecture_retriever.retrieve(
                    question
                )
            )

            architecture_citation_engine = (
                ArchitectureCitationEngine(
                    architecture_analysis
                )
            )

            architecture_citations = (
                architecture_citation_engine.generate()
            )

            return {
                "category": "ARCHITECTURE",
                "architecture": architecture_analysis,
                "architecture_context": (
                    architecture_retrieval
                ),
                "structured_architecture_context": (
                    architecture_context
                ),
                "architecture_citations": (
                    architecture_citations
                ),
            }

        # =====================================================
        # BOTH
        # =====================================================

        if classification.category == "BOTH":
            architecture_analysis = (
                self.architecture_engine.analyze()
            )

            architecture_context = (
                ArchitectureContext(
                    architecture_analysis
                )
            )

            architecture_citation_engine = (
                ArchitectureCitationEngine(
                    architecture_analysis
                )
            )

            architecture_citations = (
                architecture_citation_engine.generate()
            )

            rag_result = self.rag_pipeline.ask(
                question,
                architecture_context=(
                    architecture_context
                ),
            )

            # -------------------------------------------------
            # CODE GRAPH
            # -------------------------------------------------

            graph_context = None

            if self.code_graph_engine is not None:
                graph_context = (
                    self.code_graph_engine.build()
                )

            # -------------------------------------------------
            # GRAPH-AWARE QUERY
            # -------------------------------------------------

            graph_query_context = {}

            if self.graph_aware_query is not None:
                graph_query_context = (
                    self._get_graph_query_context(
                        question
                    )
                )

            # -------------------------------------------------
            # UNIFIED CONTEXT
            # -------------------------------------------------

            unified_context = UnifiedContext(
                rag_context=rag_result.get(
                    "rag_context",
                    [],
                ),
                architecture_context=(
                    architecture_context
                ),
                architecture_citations=(
                    architecture_citations
                ),
                symbol_context=rag_result.get(
                    "symbol_context",
                    [],
                ),
                graph_context=graph_context,
            )

            result = {
                "category": "BOTH",
                "answer": rag_result.get(
                    "answer"
                ),
                "raw_answer": rag_result.get(
                    "raw_answer"
                ),
                "citations": rag_result.get(
                    "citations",
                    [],
                ),
                "architecture_citations": (
                    architecture_citations
                ),
                "performance": rag_result.get(
                    "performance"
                ),
                "conversation_size": rag_result.get(
                    "conversation_size"
                ),
                "architecture": (
                    architecture_analysis
                ),
                "architecture_context": (
                    architecture_context
                ),
                "graph_query_context": (
                    graph_query_context
                ),
                "unified_context": (
                    unified_context
                ),
            }

            # -------------------------------------------------
            # IMPACT ANALYSIS
            # -------------------------------------------------

            if (
                self.impact_engine is not None
                and self._is_impact_question(
                    question
                )
            ):
                target = (
                    self._extract_impact_target(
                        question
                    )
                )

                if target:
                    impact_result = (
                        self.impact_engine.analyze(
                            target
                        )
                    )

                    result["impact"] = (
                        impact_result
                    )

                    result["unified_context"] = (
                        UnifiedContext(
                            rag_context=rag_result.get(
                                "rag_context",
                                [],
                            ),
                            architecture_context=(
                                architecture_context
                            ),
                            architecture_citations=(
                                architecture_citations
                            ),
                            symbol_context=rag_result.get(
                                "symbol_context",
                                [],
                            ),
                            graph_context=(
                                graph_context
                            ),
                            impact_context=(
                                impact_result
                            ),
                        )
                    )

            return result

        raise ValueError(
            f"Unsupported intelligence category: "
            f"{classification.category}"
        )

    # =========================================================
    # GRAPH QUERY CONTEXT
    # =========================================================

    def _get_graph_query_context(
        self,
        question: str,
    ):
        """
        Extract a symbol/module target from the question
        and perform the appropriate graph query.
        """

        target = self._extract_graph_target(
            question
        )

        if not target:
            return {}

        question_lower = question.lower()

        if "who calls" in question_lower:
            return {
                "callers": (
                    self.graph_aware_query.get_callers(
                        target
                    )
                )
            }

        if "what does" in question_lower and (
            "call" in question_lower
            or "calls" in question_lower
        ):
            return {
                "callees": (
                    self.graph_aware_query.get_callees(
                        target
                    )
                )
            }

        if "imports" in question_lower:
            return {
                "imports": (
                    self.graph_aware_query.get_imports(
                        target
                    )
                )
            }

        if "import" in question_lower:
            return {
                "importers": (
                    self.graph_aware_query.get_importers(
                        target
                    )
                )
            }

        if "inherit" in question_lower:
            return {
                "relationships": (
                    self.graph_aware_query.get_relationships(
                        target
                    )
                )
            }

        return {
            "relationships": (
                self.graph_aware_query.get_relationships(
                    target
                )
            )
        }

    def _extract_graph_target(
        self,
        question: str,
    ):
        """
        Extract a graph symbol/module identifier
        from a question.
        """

        words = (
            question
            .replace("?", "")
            .split()
        )

        for word in words:
            cleaned = word.strip(
                ".,:;()[]{}\"'"
            )

            if (
                ":method:" in cleaned
                or ":function:" in cleaned
                or ":class:" in cleaned
            ):
                return cleaned

            if cleaned.endswith(".py"):
                return cleaned

            if (
                cleaned.startswith("app/")
                or cleaned.startswith("tests/")
            ):
                return cleaned

            if (
                cleaned.startswith("app.")
                or cleaned.startswith("tests.")
            ):
                return cleaned

        return None

    # =========================================================
    # IMPACT
    # =========================================================

    def _is_impact_question(
        self,
        question: str,
    ) -> bool:
        question_lower = question.lower()

        impact_keywords = (
            "modify",
            "change",
            "refactor",
            "impact",
            "what happens if",
        )

        return any(
            keyword in question_lower
            for keyword in impact_keywords
        )

    def _extract_impact_target(
        self,
        question: str,
    ):
        words = (
            question
            .replace("?", "")
            .split()
        )

        for word in words:
            cleaned = word.strip(
                ".,:;()[]{}\"'"
            )

            if (
                cleaned.startswith("app/")
                or cleaned.startswith("tests/")
            ):
                return cleaned

            if (
                cleaned.startswith("app.")
                or cleaned.startswith("tests.")
            ):
                return cleaned

        return None