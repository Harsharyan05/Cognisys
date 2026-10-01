"""
Code Graph Builder

Builds a CodeGraph from extracted symbol relationships.

Author: Harsh Aryan
Project: Cognisys
"""

from app.graph.code_graph import CodeGraph


class GraphBuilder:
    """
    Converts symbol relationships into a CodeGraph.

    The builder does not parse source code directly.
    Relationship extraction is handled separately by
    SymbolRelationshipExtractor.
    """

    def __init__(self):
        pass

    def build(self, relationships):
        """
        Build a CodeGraph from a list of relationships.

        Parameters
        ----------
        relationships : list[dict]
            Extracted symbol/module relationships.

        Returns
        -------
        CodeGraph
            Populated code graph.
        """

        graph = CodeGraph()

        for relationship in relationships:

            if not isinstance(relationship, dict):
                continue

            source = relationship.get("source")
            target = relationship.get("target")
            relationship_type = relationship.get("type")

            if not source or not target or not relationship_type:
                continue

            graph.add_node(
                source,
                node_type=self._infer_node_type(source),
            )

            graph.add_node(
                target,
                node_type=self._infer_node_type(target),
            )

            graph.add_edge(
                source,
                target,
                relationship_type=relationship_type,
            )

        return graph

    def _infer_node_type(self, node_id):
        """
        Infer a basic node type from its identifier.
        """

        if ":method:" in node_id:
            return "method"

        if ":function:" in node_id:
            return "function"

        if ":class:" in node_id:
            return "class"

        if node_id.endswith(".py"):
            return "module"

        return "unknown"