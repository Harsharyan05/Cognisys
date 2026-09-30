class UnifiedContext:
    """
    Combines all intelligence sources for the Cognisys
    intelligence layer.

    Current context sources:
    - RAG context
    - Architecture context

    Future sources:
    - Symbol context
    - Impact context
    - Dependency context
    """

    def __init__(
        self,
        rag_context=None,
        architecture_context=None,
        symbol_context=None,
        impact_context=None,
    ):
        self.rag_context = rag_context or []
        self.architecture_context = architecture_context
        self.symbol_context = symbol_context or []
        self.impact_context = impact_context

    def get_rag_context(self):
        """Return semantic/code retrieval context."""
        return self.rag_context

    def get_architecture_context(self):
        """Return architecture intelligence context."""
        return self.architecture_context

    def get_symbol_context(self):
        """Return symbol-level retrieval context."""
        return self.symbol_context

    def get_impact_context(self):
        """Return impact analysis context."""
        return self.impact_context

    def has_rag_context(self):
        """Return whether RAG context is available."""
        return bool(self.rag_context)

    def has_architecture_context(self):
        """Return whether architecture context is available."""
        return self.architecture_context is not None

    def has_symbol_context(self):
        """Return whether symbol context is available."""
        return bool(self.symbol_context)

    def has_impact_context(self):
        """Return whether impact context is available."""
        return self.impact_context is not None

    def to_dict(self):
        """
        Convert the unified context into a serializable
        dictionary for downstream prompt/context builders.
        """
        return {
            "rag_context": self.rag_context,
            "architecture_context": self.architecture_context,
            "symbol_context": self.symbol_context,
            "impact_context": self.impact_context,
        }