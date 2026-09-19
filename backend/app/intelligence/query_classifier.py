from dataclasses import dataclass


@dataclass
class IntelligenceQueryClassification:
    category: str
    confidence: float


class IntelligenceQueryClassifier:
    """
    Determines which Cognisys intelligence source should handle
    a repository question.

    Categories:
        RAG            -> semantic/code knowledge
        ARCHITECTURE   -> architecture/dependency knowledge
        BOTH           -> requires both sources
    """

    ARCHITECTURE_KEYWORDS = {
        "architecture",
        "layer",
        "layers",
        "dependency",
        "dependencies",
        "depend",
        "depends",
        "dependent",
        "module",
        "modules",
        "circular",
        "coupling",
        "hotspot",
        "pattern",
        "patterns",
        "structure",
        "impact",
    }

    BOTH_KEYWORDS = {
        "modify",
        "change",
        "refactor",
        "impact",
        "happens if",
        "authentication flow",
        "flow",
    }

    def classify(self, question: str) -> IntelligenceQueryClassification:
        question_lower = question.lower().strip()

        if not question_lower:
            return IntelligenceQueryClassification(
                category="RAG",
                confidence=0.5,
            )

        # Questions that require both code understanding
        # and architectural understanding.
        if any(keyword in question_lower for keyword in self.BOTH_KEYWORDS):
            return IntelligenceQueryClassification(
                category="BOTH",
                confidence=0.9,
            )

        # Architecture-specific questions.
        if any(
            keyword in question_lower
            for keyword in self.ARCHITECTURE_KEYWORDS
        ):
            return IntelligenceQueryClassification(
                category="ARCHITECTURE",
                confidence=0.9,
            )

        # Default: use the existing RAG system.
        return IntelligenceQueryClassification(
            category="RAG",
            confidence=0.8,
        )