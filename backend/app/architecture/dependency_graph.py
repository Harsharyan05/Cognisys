"""
Dependency Graph

Author: Harsh Aryan
Project: Cognisys
"""

from pathlib import Path
from typing import Dict, List
import ast


class DependencyGraph:

    IGNORE_DIRS = {
        ".git",
        "__pycache__",
        ".venv",
        "venv",
        "node_modules",
        ".idea",
        ".vscode",
        "tests",
    }

    def __init__(self, repository_path: str):
        self.repository_path = Path(repository_path)

    
    def build(self) -> Dict[str, List[str]]:
        graph = {}

        for file in self.repository_path.rglob("*.py"):

            # Ignore unwanted directories
            if any(part in self.IGNORE_DIRS for part in file.parts):
                continue

            # Ignore malformed paths caused by accidental path concatenation
            if ".pyapp" in str(file).lower():
                continue

            # Ignore test files
            if file.name.startswith("test_"):
                continue

            module_name = self.get_module_name(file)

            try:
                tree = ast.parse(file.read_text(encoding="utf-8"))

                visitor = ImportVisitor()
                visitor.visit(tree)

                graph[module_name] = sorted(visitor.imports)

            except Exception:
                graph[module_name] = []

        return graph

    def get_module_name(self, file: Path) -> str:
        """
        Convert a Python file path into a module name.

        Example:
        app/parser/python_ast_parser.py
        ->
        app.parser.python_ast_parser
        """

        relative_path = file.relative_to(self.repository_path)

        return ".".join(
            relative_path.with_suffix("").parts
        )


class ImportVisitor(ast.NodeVisitor):

    def __init__(self):
        self.imports = set()

    def visit_Import(self, node):

        for alias in node.names:
            self.imports.add(alias.name)

        self.generic_visit(node)

    def visit_ImportFrom(self, node):

        if node.module:
            self.imports.add(node.module)

        self.generic_visit(node)