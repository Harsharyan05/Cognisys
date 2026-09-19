class UnifiedContext:
    """
    Combines RAG context and architecture context
    for the Cognisys intelligence layer.
    """

    def __init__(self, rag_context, architecture_context):
        self.rag_context = rag_context
        self.architecture_context = architecture_context

    def get_rag_context(self):
        return self.rag_context

    def get_architecture_context(self):
        return self.architecture_context