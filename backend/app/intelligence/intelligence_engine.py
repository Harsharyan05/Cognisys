from app.intelligence.architecture_context import ArchitectureContext
from app.intelligence.architecture_aware_retriever import (
    ArchitectureAwareRetriever,
)
from app.intelligence.query_classifier import IntelligenceQueryClassifier


class IntelligenceEngine:
    """
    High-level orchestrator for Cognisys repository intelligence.

    Routes questions to:
    - RAG
    - Architecture
    - Both
    - Impact-aware analysis through the Both path

    Architecture results are wrapped in ArchitectureContext
    so they can be combined with the RAG pipeline.
    """

    def __init__(
        self,
        rag_pipeline,
        architecture_engine,
        impact_engine=None,
    ):
        self.rag_pipeline = rag_pipeline
        self.architecture_engine = architecture_engine
        self.impact_engine = impact_engine
        self.query_classifier = IntelligenceQueryClassifier()

    def ask(
        self,
        question: str,
    ):
        classification = self.query_classifier.classify(
            question
        )

        # ---------------------------------------------------------
        # RAG
        # ---------------------------------------------------------

        if classification.category == "RAG":

            result = self.rag_pipeline.ask(
                question
            )

            return {
                "category": "RAG",
                **result,
            }

        # ---------------------------------------------------------
        # ARCHITECTURE
        # ---------------------------------------------------------

        if classification.category == "ARCHITECTURE":

            architecture_analysis = (
                self.architecture_engine.analyze()
            )

            architecture_context = ArchitectureContext(
                architecture_analysis
            )

            architecture_retriever = ArchitectureAwareRetriever(
                architecture_analysis
            )

            architecture_retrieval = (
                architecture_retriever.retrieve(
                    question
                )
            )

            return {
                "category": "ARCHITECTURE",
                "architecture": architecture_analysis,
                "architecture_context": architecture_retrieval,
                "structured_architecture_context": architecture_context,
            }

        # ---------------------------------------------------------
        # BOTH
        # ---------------------------------------------------------

        if classification.category == "BOTH":

            architecture_analysis = (
                self.architecture_engine.analyze()
            )

            architecture_context = ArchitectureContext(
                architecture_analysis
            )

            rag_result = self.rag_pipeline.ask(
                question,
                architecture_context=architecture_context,
            )

            result = {
                "category": "BOTH",
                "answer": rag_result.get("answer"),
                "raw_answer": rag_result.get("raw_answer"),
                "citations": rag_result.get(
                    "citations",
                    [],
                ),
                "performance": rag_result.get(
                    "performance"
                ),
                "conversation_size": rag_result.get(
                    "conversation_size"
                ),
                "architecture": architecture_analysis,
                "architecture_context": architecture_context,
            }

            # -----------------------------------------------------
            # Impact Analysis
            # -----------------------------------------------------

            if (
                self.impact_engine is not None
                and self._is_impact_question(question)
            ):
                target = self._extract_impact_target(
                    question
                )

                if target:
                    impact_result = self.impact_engine.analyze(
                        target
                    )

                    result["impact"] = impact_result

            return result

        raise ValueError(
            f"Unsupported intelligence category: "
            f"{classification.category}"
        )

    def _is_impact_question(
        self,
        question: str,
    ) -> bool:
        """
        Determine whether the question asks about the impact
        of modifying or changing something.
        """

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
        """
        Extract the repository target from a question.

        Currently supports the explicit repository/module path
        form used by the impact-analysis interface.
        """

        words = question.replace("?", "").split()

        for word in words:
            cleaned = word.strip(
                ".,:;()[]{}\"'"
            )

            if (
                "." in cleaned
                and (
                    cleaned.startswith("app.")
                    or cleaned.startswith("tests.")
                )
            ):
                return cleaned

        return None