"""
Graph-Aware Query Layer

Provides a clean intelligence-facing interface over
the Code Graph query layer.

Author: Harsh Aryan
Project: Cognisys
"""


class GraphAwareQuery:
    """
    Provides graph-aware repository queries.

    This class delegates graph operations to GraphQuery
    while providing a stable interface for the intelligence
    layer.
    """

    def __init__(self, graph_query):
        self.graph_query = graph_query

    # ========================================================
    # CALL RELATIONSHIPS
    # ========================================================

    def get_callers(self, symbol_id):
        """
        Return symbols that call the given symbol.
        """

        return self.graph_query.get_callers(
            symbol_id
        )

    def get_callees(self, symbol_id):
        """
        Return symbols called by the given symbol.
        """

        return self.graph_query.get_callees(
            symbol_id
        )

    # ========================================================
    # IMPORT RELATIONSHIPS
    # ========================================================

    def get_imports(self, module):
        """
        Return modules imported by the given module.
        """

        return self.graph_query.get_imports(
            module
        )

    def get_importers(self, module):
        """
        Return modules that import the given module.
        """

        return self.graph_query.get_importers(
            module
        )

    # ========================================================
    # INHERITANCE RELATIONSHIPS
    # ========================================================

    def get_parent_classes(self, symbol_id):
        """
        Return parent classes of the given class.
        """

        return self.graph_query.get_parent_classes(
            symbol_id
        )

    def get_child_classes(self, symbol_id):
        """
        Return child classes of the given class.
        """

        return self.graph_query.get_child_classes(
            symbol_id
        )

    # ========================================================
    # GENERAL RELATIONSHIPS
    # ========================================================

    def get_relationships(self, symbol_id):
        """
        Return all graph relationships involving a symbol.
        """

        return self.graph_query.get_relationships(
            symbol_id
        )