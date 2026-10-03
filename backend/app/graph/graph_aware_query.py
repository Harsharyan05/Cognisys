"""
Graph-aware query interface.

Author: Harsh Aryan
Project: Cognisys
"""


class GraphAwareQuery:
    """
    High-level interface for querying the Cognisys code graph.
    """

    def __init__(self, graph_query):
        self.graph_query = graph_query

    def get_callers(self, symbol_id):
        return self.graph_query.get_callers(symbol_id)

    def get_callees(self, symbol_id):
        return self.graph_query.get_callees(symbol_id)

    def get_imports(self, module):
        return self.graph_query.get_imports(module)

    def get_importers(self, module):
        return self.graph_query.get_importers(module)

    def get_parent_classes(self, symbol_id):
        return self.graph_query.get_parent_classes(symbol_id)

    def get_child_classes(self, symbol_id):
        return self.graph_query.get_child_classes(symbol_id)

    def get_relationships(self, symbol_id):
        return self.graph_query.get_relationships(symbol_id)