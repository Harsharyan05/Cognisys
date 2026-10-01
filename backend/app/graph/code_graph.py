"""
Code Graph

Represents code-level relationships between files,
classes, functions, and methods.

Supported relationships:
- CALLS
- IMPORTS
- INHERITS

Author: Harsh Aryan
Project: Cognisys
"""


class CodeGraph:
    """
    In-memory graph representing relationships between
    code entities.
    """

    def __init__(self):
        self.nodes = {}
        self.edges = []

    # ---------------------------------------------------------
    # Nodes
    # ---------------------------------------------------------

    def add_node(self, node_id, node_type=None):
        """Add a node to the graph."""

        if node_id not in self.nodes:
            self.nodes[node_id] = {
                "id": node_id,
                "type": node_type,
            }

    def has_node(self, node_id):
        """Check whether a node exists."""

        return node_id in self.nodes

    # ---------------------------------------------------------
    # Edges
    # ---------------------------------------------------------

    def add_edge(
        self,
        source,
        target,
        relationship_type,
    ):
        """Add a relationship between two nodes."""

        self.add_node(source)
        self.add_node(target)

        edge = {
            "source": source,
            "target": target,
            "type": relationship_type,
        }

        if edge not in self.edges:
            self.edges.append(edge)

    def has_edge(
        self,
        source,
        target,
        relationship_type,
    ):
        """Check whether a relationship exists."""

        return {
            "source": source,
            "target": target,
            "type": relationship_type,
        } in self.edges

    # ---------------------------------------------------------
    # CALL Relationships
    # ---------------------------------------------------------

    def get_callees(self, symbol_id):
        """Return symbols called by the given symbol."""

        return [
            edge["target"]
            for edge in self.edges
            if (
                edge["source"] == symbol_id
                and edge["type"] == "CALLS"
            )
        ]

    def get_callers(self, symbol_id):
        """Return symbols that call the given symbol."""

        return [
            edge["source"]
            for edge in self.edges
            if (
                edge["target"] == symbol_id
                and edge["type"] == "CALLS"
            )
        ]

    # ---------------------------------------------------------
    # IMPORT Relationships
    # ---------------------------------------------------------

    def get_imports(self, module):
        """Return modules imported by the given module."""

        return [
            edge["target"]
            for edge in self.edges
            if (
                edge["source"] == module
                and edge["type"] == "IMPORTS"
            )
        ]

    def get_importers(self, module):
        """Return modules that import the given module."""

        return [
            edge["source"]
            for edge in self.edges
            if (
                edge["target"] == module
                and edge["type"] == "IMPORTS"
            )
        ]

    # ---------------------------------------------------------
    # INHERITANCE Relationships
    # ---------------------------------------------------------

    def get_parent_classes(self, symbol_id):
        """Return parent classes of the given class."""

        return [
            edge["target"]
            for edge in self.edges
            if (
                edge["source"] == symbol_id
                and edge["type"] == "INHERITS"
            )
        ]

    def get_child_classes(self, symbol_id):
        """Return child classes of the given class."""

        return [
            edge["source"]
            for edge in self.edges
            if (
                edge["target"] == symbol_id
                and edge["type"] == "INHERITS"
            )
        ]

    # ---------------------------------------------------------
    # General Queries
    # ---------------------------------------------------------

    def get_edges(self):
        """Return all graph edges."""

        return list(self.edges)

    def get_nodes(self):
        """Return all graph nodes."""

        return list(self.nodes.values())