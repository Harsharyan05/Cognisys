class UnifiedContext:
    """
    Combines all intelligence sources for the Cognisys
    intelligence layer.

    Current context sources:
    - RAG context
    - Architecture context
    - Architecture citations
    - Symbol context
    - Code graph context
    - Impact context
    """

    def __init__(
        self,
        rag_context=None,
        architecture_context=None,
        architecture_citations=None,
        symbol_context=None,
        graph_context=None,
        impact_context=None,
    ):
        self.rag_context = rag_context or []
        self.architecture_context = architecture_context
        self.architecture_citations = (
            architecture_citations or []
        )
        self.symbol_context = symbol_context or []
        self.graph_context = graph_context
        self.impact_context = impact_context

    # ========================================================
    # RAG
    # ========================================================

    def get_rag_context(self):
        return self.rag_context

    # ========================================================
    # ARCHITECTURE
    # ========================================================

    def get_architecture_context(self):
        return self.architecture_context

    def get_architecture_citations(self):
        return self.architecture_citations

    # ========================================================
    # SYMBOL
    # ========================================================

    def get_symbol_context(self):
        return self.symbol_context

    # ========================================================
    # GRAPH
    # ========================================================

    def get_graph_context(self):
        return self.graph_context

    # ========================================================
    # IMPACT
    # ========================================================

    def get_impact_context(self):
        return self.impact_context

    # ========================================================
    # EXISTENCE CHECKS
    # ========================================================

    def has_rag_context(self):
        return bool(self.rag_context)

    def has_architecture_context(self):
        return self.architecture_context is not None

    def has_architecture_citations(self):
        return bool(self.architecture_citations)

    def has_symbol_context(self):
        return bool(self.symbol_context)

    def has_graph_context(self):
        return self.graph_context is not None

    def has_impact_context(self):
        return self.impact_context is not None

    # ========================================================
    # SERIALIZATION
    # ========================================================

    def to_dict(self):
        return {
            "rag_context": self.rag_context,
            "architecture_context": self.architecture_context,
            "architecture_citations": (
                self.architecture_citations
            ),
            "symbol_context": self.symbol_context,
            "graph_context": self.graph_context,
            "impact_context": self.impact_context,
        }