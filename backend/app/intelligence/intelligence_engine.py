from app.intelligence.architecture_context import ArchitectureContext
from app.intelligence.query_classifier import IntelligenceQueryClassifier


class IntelligenceEngine:
    """
    High-level orchestrator for Cognisys repository intelligence.

    Routes questions to:
    - RAG
    - Architecture
    - Both

    Architecture results are wrapped in ArchitectureContext
    so they can be combined with the RAG pipeline.
    """

    def __init__(
        self,
        rag_pipeline,
        architecture_engine,
    ):
        self.rag_pipeline = rag_pipeline
        self.architecture_engine = architecture_engine
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

            return {
                "category": "ARCHITECTURE",
                "architecture": architecture_analysis,
                "architecture_context": architecture_context,
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

            return {
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

        raise ValueError(
            f"Unsupported intelligence category: "
            f"{classification.category}"
        )