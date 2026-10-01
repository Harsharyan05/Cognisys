"""
Code Graph Query Layer

Provides a clean query interface over CodeGraph.

Author: Harsh Aryan
Project: Cognisys
"""


class GraphQuery:
    """
    Query interface for Cognisys CodeGraph.
    """

    def __init__(self, graph):
        self.graph = graph

    # ---------------------------------------------------------
    # CALL Relationships
    # ---------------------------------------------------------

    def get_callers(self, symbol_id):
        """
        Return symbols that call the given symbol.
        """

        return self.graph.get_callers(
            symbol_id
        )

    def get_callees(self, symbol_id):
        """
        Return symbols called by the given symbol.
        """

        return self.graph.get_callees(
            symbol_id
        )

    # ---------------------------------------------------------
    # IMPORT Relationships
    # ---------------------------------------------------------

    def get_imports(self, module):
        """
        Return modules imported by the given module.
        """

        return self.graph.get_imports(
            module
        )

    def get_importers(self, module):
        """
        Return modules that import the given module.
        """

        return self.graph.get_importers(
            module
        )

    # ---------------------------------------------------------
    # INHERITANCE Relationships
    # ---------------------------------------------------------

    def get_parent_classes(self, symbol_id):
        """
        Return parent classes of the given class.
        """

        return self.graph.get_parent_classes(
            symbol_id
        )

    def get_child_classes(self, symbol_id):
        """
        Return child classes of the given class.
        """

        return self.graph.get_child_classes(
            symbol_id
        )

    # ---------------------------------------------------------
    # General Relationships
    # ---------------------------------------------------------

    def get_relationships(self, symbol_id):
        """
        Return all relationships involving a symbol.
        """

        relationships = []

        for edge in self.graph.get_edges():

            if (
                edge["source"] == symbol_id
                or edge["target"] == symbol_id
            ):
                relationships.append(edge)

        return relationships