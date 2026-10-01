"""
Code Graph Engine

Orchestrates symbol relationship extraction and
code graph construction.

Author: Harsh Aryan
Project: Cognisys
"""

from pathlib import Path

from app.parser.symbol_relationship_extractor import (
    SymbolRelationshipExtractor,
)
from app.graph.graph_builder import GraphBuilder


class CodeGraphEngine:
    """
    Builds a CodeGraph from a repository.

    Pipeline:

        Repository
            ↓
        SymbolRelationshipExtractor
            ↓
        Relationships
            ↓
        GraphBuilder
            ↓
        CodeGraph
    """

    def __init__(self, repository_path):
        self.repository_path = Path(repository_path)

        self.relationship_extractor = (
            SymbolRelationshipExtractor(
                self.repository_path
            )
        )

        self.graph_builder = GraphBuilder()

    def build(self):
        """
        Extract relationships and build the code graph.
        """

        relationships = (
            self.relationship_extractor.extract()
        )

        return self.graph_builder.build(
            relationships
        )