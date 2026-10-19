
"""
Symbol Extractor

Author: Harsh Aryan
Project: Cognisys
"""

import ast
from pathlib import Path


class SymbolExtractor:
    """
    Extracts classes and functions from Python files
    along with source code, line numbers, parent class
    relationships, and stable symbol IDs.
    """

    IGNORED_DIRECTORIES = {
        ".git",
        ".venv",
        "venv",
        "__pycache__",
        "node_modules",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        "storage",
    }

    def extract(self, repository_path: str):
        root = Path(repository_path)
        symbols = {}

        for file in root.rglob("*.py"):
            relative = file.relative_to(root)

            # Skip generated, environment, and cache directories.
            if any(
                part in self.IGNORED_DIRECTORIES
                for part in relative.parts
            ):
                continue

            relative_path = str(relative)

            try:
                source = file.read_text(
                    encoding="utf-8",
                    errors="ignore",
                )
                tree = ast.parse(source)
            except (OSError, SyntaxError, ValueError):
                continue

            source_lines = source.splitlines()

            file_symbols = {
                "classes": [],
                "functions": [],
            }

            self._extract_nodes(
                tree=tree,
                source_lines=source_lines,
                file_symbols=file_symbols,
                parent_class=None,
                relative_path=relative_path,
            )

            symbols[relative_path] = file_symbols

        return symbols

    def _extract_nodes(
        self,
        tree,
        source_lines,
        file_symbols,
        parent_class=None,
        relative_path=None,
    ):
        """Traverse the AST while preserving class context."""

        for node in tree.body:

            if isinstance(node, ast.ClassDef):
                code = self._get_source_code(source_lines, node)

                file_symbols["classes"].append({
                    "id": f"{relative_path}:class:{node.name}",
                    "name": node.name,
                    "type": "class",
                    "line": node.lineno,
                    "end_line": node.end_lineno,
                    "code": code,
                })

                self._extract_nodes(
                    tree=node,
                    source_lines=source_lines,
                    file_symbols=file_symbols,
                    parent_class=node.name,
                    relative_path=relative_path,
                )

            elif isinstance(
                node,
                (ast.FunctionDef, ast.AsyncFunctionDef),
            ):
                code = self._get_source_code(source_lines, node)

                if parent_class:
                    symbol_id = (
                        f"{relative_path}:method:"
                        f"{parent_class}.{node.name}"
                    )
                    symbol_type = "method"
                else:
                    symbol_id = (
                        f"{relative_path}:function:{node.name}"
                    )
                    symbol_type = "function"

                file_symbols["functions"].append({
                    "id": symbol_id,
                    "name": node.name,
                    "type": symbol_type,
                    "line": node.lineno,
                    "end_line": node.end_lineno,
                    "code": code,
                    "parent_class": parent_class,
                })

            elif isinstance(
                node,
                (ast.If, ast.For, ast.While, ast.Try),
            ):
                self._extract_nodes(
                    tree=node,
                    source_lines=source_lines,
                    file_symbols=file_symbols,
                    parent_class=parent_class,
                    relative_path=relative_path,
                )

    def _get_source_code(self, source_lines, node):
        """Return the exact source lines belonging to a node."""

        return "\n".join(
            source_lines[node.lineno - 1:node.end_lineno]
        )

