from dataclasses import dataclass


@dataclass
class ClassificationResult:
    """
    Result returned by the intelligence query classifier.
    """

    category: str
    confidence: float = 1.0


class IntelligenceQueryClassifier:
    """
    Classifies repository questions into:

    - RAG
    - ARCHITECTURE
    - BOTH

    Graph-aware questions are routed through BOTH so that
    RAG, architecture, and code-graph intelligence can
    contribute to the answer.
    """

    def classify(self, question: str):
        question_lower = question.lower()

        # =====================================================
        # GRAPH-AWARE / COMBINED QUERIES
        # =====================================================

        graph_keywords = (
            "who calls",
            "callers",
            "callees",
            "calls",
            "import",
            "imports",
            "imported by",
            "inherit",
            "inherits",
            "inherited by",
            "parent class",
            "child class",
        )

        graph_query = any(
            keyword in question_lower
            for keyword in graph_keywords
        )

        # "What does X call?" is graph-aware only when
        # the question explicitly asks about a call relationship.
        if (
            "what does" in question_lower
            and " call" in question_lower
        ):
            graph_query = True

        # =====================================================
        # BOTH QUERIES
        # =====================================================

        both_keywords = (
            "modify",
            "change",
            "refactor",
            "impact",
            "what happens if",
            "authentication flow",
            "flow",
        )

        both_query = any(
            keyword in question_lower
            for keyword in both_keywords
        )

        if graph_query or both_query:
            return ClassificationResult(
                category="BOTH",
                confidence=1.0,
            )

        # =====================================================
        # ARCHITECTURE QUERIES
        # =====================================================

        architecture_keywords = (
            "architecture",
            "layer",
            "layers",
            "dependency",
            "dependencies",
            "module",
            "modules",
            "circular",
            "coupling",
            "hotspot",
            "hotspots",
            "pattern",
            "patterns",
            "structure",
        )

        if any(
            keyword in question_lower
            for keyword in architecture_keywords
        ):
            return ClassificationResult(
                category="ARCHITECTURE",
                confidence=1.0,
            )

        # =====================================================
        # DEFAULT → RAG
        # =====================================================

        return ClassificationResult(
            category="RAG",
            confidence=1.0,
        )