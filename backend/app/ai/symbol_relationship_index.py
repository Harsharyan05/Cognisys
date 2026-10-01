"""
Symbol Relationship Index

Provides queryable access to relationships extracted
from a Python repository.

Supported relationships:
- CALLS
- CALLED_BY
- IMPORTS
- IMPORTED_BY
- INHERITS
- INHERITED_BY

Author: Harsh Aryan
Project: Cognisys
"""


class SymbolRelationshipIndex:
    """
    Query layer over extracted symbol relationships.

    The index does not parse source code. It only indexes
    relationships produced by SymbolRelationshipExtractor.
    """

    def __init__(self, relationships=None):
        self.relationships = relationships or []

        self._relationships_by_source = {}
        self._relationships_by_target = {}

        self._build_index()

    # ---------------------------------------------------------
    # Index Construction
    # ---------------------------------------------------------

    def _build_index(self):
        for relationship in self.relationships:
            source = relationship.get("source")
            target = relationship.get("target")

            if not source or not target:
                continue

            self._relationships_by_source.setdefault(
                source,
                [],
            ).append(relationship)

            self._relationships_by_target.setdefault(
                target,
                [],
            ).append(relationship)

    # ---------------------------------------------------------
    # General Relationship Query
    # ---------------------------------------------------------

    def get_relationships(self, symbol_id):
        """
        Return all relationships involving a symbol.
        """

        relationships = []

        relationships.extend(
            self._relationships_by_source.get(
                symbol_id,
                [],
            )
        )

        relationships.extend(
            self._relationships_by_target.get(
                symbol_id,
                [],
            )
        )

        return self._deduplicate(relationships)

    # ---------------------------------------------------------
    # CALL Relationships
    # ---------------------------------------------------------

    def get_callers(self, symbol_id):
        """
        Return symbols that call the given symbol.
        """

        return [
            relationship["source"]
            for relationship in self._relationships_by_target.get(
                symbol_id,
                [],
            )
            if relationship.get("type") == "CALLS"
        ]

    def get_callees(self, symbol_id):
        """
        Return symbols called by the given symbol.
        """

        return [
            relationship["target"]
            for relationship in self._relationships_by_source.get(
                symbol_id,
                [],
            )
            if relationship.get("type") == "CALLS"
        ]

    # ---------------------------------------------------------
    # Import Relationships
    # ---------------------------------------------------------

    def get_importers(self, module):
        """
        Return modules that import the given module.
        """

        return [
            relationship["source"]
            for relationship in self._relationships_by_target.get(
                module,
                [],
            )
            if relationship.get("type") == "IMPORTS"
        ]

    def get_imports(self, module):
        """
        Return modules imported by the given module.
        """

        return [
            relationship["target"]
            for relationship in self._relationships_by_source.get(
                module,
                [],
            )
            if relationship.get("type") == "IMPORTS"
        ]

    # ---------------------------------------------------------
    # Inheritance Relationships
    # ---------------------------------------------------------

    def get_parent_classes(self, symbol_id):
        """
        Return parent classes inherited by the given class.
        """

        return [
            relationship["target"]
            for relationship in self._relationships_by_source.get(
                symbol_id,
                [],
            )
            if relationship.get("type") == "INHERITS"
        ]

    def get_child_classes(self, symbol_id):
        """
        Return classes that inherit from the given class.
        """

        return [
            relationship["source"]
            for relationship in self._relationships_by_target.get(
                symbol_id,
                [],
            )
            if relationship.get("type") == "INHERITS"
        ]

    # ---------------------------------------------------------
    # Relationship Type Queries
    # ---------------------------------------------------------

    def get_relationships_by_type(
        self,
        relationship_type,
    ):
        """
        Return all relationships of a specific type.
        """

        return [
            relationship
            for relationship in self.relationships
            if relationship.get("type")
            == relationship_type
        ]

    # ---------------------------------------------------------
    # Deduplication
    # ---------------------------------------------------------

    def _deduplicate(self, relationships):
        unique = []
        seen = set()

        for relationship in relationships:
            key = (
                relationship.get("source"),
                relationship.get("target"),
                relationship.get("type"),
            )

            if key in seen:
                continue

            seen.add(key)
            unique.append(relationship)

        return unique