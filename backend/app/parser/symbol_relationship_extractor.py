"""
Symbol Relationship Extractor

Extracts relationships between symbols and modules
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

from pathlib import Path
import ast


class SymbolRelationshipExtractor:
    """
    Extracts code-level relationships from a Python repository.
    """

    def __init__(self, repository_path):
        self.repository_path = Path(repository_path)

    def extract(self):
        """
        Extract all supported relationships from the repository.
        """

        relationships = []

        parsed_files = self._parse_repository()

        symbol_table = self._build_symbol_table(
            parsed_files
        )

        relationships.extend(
            self._extract_call_relationships(
                parsed_files,
                symbol_table,
            )
        )

        relationships.extend(
            self._extract_import_relationships(
                parsed_files,
            )
        )

        relationships.extend(
            self._extract_inheritance_relationships(
                parsed_files,
                symbol_table,
            )
        )

        return self._deduplicate(
            relationships
        )

    # ---------------------------------------------------------
    # Repository Parsing
    # ---------------------------------------------------------

    def _parse_repository(self):
        parsed_files = {}

        for file_path in self.repository_path.rglob("*.py"):

            relative_path = str(
                file_path.relative_to(
                    self.repository_path
                )
            )

            try:
                source = file_path.read_text(
                    encoding="utf-8",
                    errors="ignore",
                )

                tree = ast.parse(source)

            except (SyntaxError, UnicodeDecodeError):
                continue

            parsed_files[relative_path] = tree

        return parsed_files

    # ---------------------------------------------------------
    # Symbol Table
    # ---------------------------------------------------------

    def _build_symbol_table(self, parsed_files):
        symbol_table = {}

        for relative_path, tree in parsed_files.items():

            for node in ast.walk(tree):

                if isinstance(
                    node,
                    (ast.FunctionDef, ast.AsyncFunctionDef),
                ):
                    symbol_id = (
                        f"{relative_path}:function:"
                        f"{node.name}"
                    )

                    symbol_table[node.name] = symbol_id

                elif isinstance(
                    node,
                    ast.ClassDef,
                ):
                    symbol_id = (
                        f"{relative_path}:class:"
                        f"{node.name}"
                    )

                    symbol_table[node.name] = symbol_id

        return symbol_table

    # ---------------------------------------------------------
    # CALLS
    # ---------------------------------------------------------

    def _extract_call_relationships(
        self,
        parsed_files,
        symbol_table,
    ):
        relationships = []

        for relative_path, tree in parsed_files.items():

            for node in ast.walk(tree):

                if not isinstance(
                    node,
                    (
                        ast.FunctionDef,
                        ast.AsyncFunctionDef,
                    ),
                ):
                    continue

                source_symbol = (
                    f"{relative_path}:function:"
                    f"{node.name}"
                )

                for child in ast.walk(node):

                    if not isinstance(
                        child,
                        ast.Call,
                    ):
                        continue

                    target_name = self._get_call_name(
                        child
                    )

                    if (
                        target_name
                        and target_name in symbol_table
                    ):
                        target_symbol = symbol_table[
                            target_name
                        ]

                        relationships.append(
                            {
                                "source": source_symbol,
                                "target": target_symbol,
                                "type": "CALLS",
                            }
                        )

        reverse_relationships = []

        for relationship in relationships:
            reverse_relationships.append(
                {
                    "source": relationship["target"],
                    "target": relationship["source"],
                    "type": "CALLED_BY",
                }
            )

        return relationships + reverse_relationships
    def _get_call_name(self, node):
        if isinstance(node.func, ast.Name):
            return node.func.id

        if isinstance(node.func, ast.Attribute):
            return node.func.attr

        return None

    # ---------------------------------------------------------
    # IMPORTS
    # ---------------------------------------------------------

    def _extract_import_relationships(
        self,
        parsed_files,
    ):
        relationships = []

        module_map = {
            Path(path).stem: path
            for path in parsed_files
        }

        for relative_path, tree in parsed_files.items():

            for node in ast.walk(tree):

                imported_module = None

                if isinstance(
                    node,
                    ast.Import,
                ):
                    for alias in node.names:

                        imported_module = (
                            alias.name.split(".")[0]
                        )

                        target = module_map.get(
                            imported_module
                        )

                        if target:
                            relationships.append(
                                {
                                    "source": relative_path,
                                    "target": target,
                                    "type": "IMPORTS",
                                }
                            )

                elif isinstance(
                    node,
                    ast.ImportFrom,
                ):
                    if node.module:

                        imported_module = (
                            node.module.split(".")[0]
                        )

                        target = module_map.get(
                            imported_module
                        )

                        if target:
                            relationships.append(
                                {
                                    "source": relative_path,
                                    "target": target,
                                    "type": "IMPORTS",
                                }
                            )

        reverse_relationships = []

        for relationship in relationships:
            reverse_relationships.append(
                {
                    "source": relationship["target"],
                    "target": relationship["source"],
                    "type": "IMPORTED_BY",
                }
            )

        return relationships + reverse_relationships

    # ---------------------------------------------------------
    # INHERITS
    # ---------------------------------------------------------

    def _extract_inheritance_relationships(
        self,
        parsed_files,
        symbol_table,
    ):
        relationships = []

        for relative_path, tree in parsed_files.items():

            for node in ast.walk(tree):

                if not isinstance(
                    node,
                    ast.ClassDef,
                ):
                    continue

                source = (
                    f"{relative_path}:class:"
                    f"{node.name}"
                )

                for base in node.bases:

                    base_name = self._get_name(
                        base
                    )

                    if (
                        base_name
                        and base_name in symbol_table
                    ):
                        target = symbol_table[
                            base_name
                        ]

                        relationships.append(
                            {
                                "source": source,
                                "target": target,
                                "type": "INHERITS",
                            }
                        )

                        relationships.append(
                            {
                                "source": target,
                                "target": source,
                                "type": "INHERITED_BY",
                            }
                        )

        return relationships

    def _get_name(self, node):
        if isinstance(node, ast.Name):
            return node.id

        if isinstance(node, ast.Attribute):
            return node.attr

        return None

    # ---------------------------------------------------------
    # Deduplication
    # ---------------------------------------------------------

    def _deduplicate(self, relationships):
        unique = []
        seen = set()

        for relationship in relationships:

            key = (
                relationship["source"],
                relationship["target"],
                relationship["type"],
            )

            if key in seen:
                continue

            seen.add(key)
            unique.append(relationship)

        return unique