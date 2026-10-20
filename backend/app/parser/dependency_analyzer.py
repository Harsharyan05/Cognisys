
"""
Dependency Analyzer

Author: Harsh Aryan
Project: Cognisys
"""

import ast
from pathlib import Path


class DependencyAnalyzer:
    """
    Extract Python import relationships from a repository.

    Identifies:
    - Standard and third-party imports
    - Internal repository module imports
    - Relative imports
    - Import type and source location
    """

    IGNORE_DIRS = {
        ".git",
        "__pycache__",
        ".venv",
        "venv",
        "node_modules",
        ".idea",
        ".vscode",
        ".pytest_cache",
        "dist",
        "build",
    }

    def analyze(self, repository_path: str) -> dict:
        """
        Return imports for each Python file.

        The original file -> list of import names structure is preserved.
        """
        root = Path(repository_path).resolve()

        if not root.is_dir():
            raise NotADirectoryError(
                f"Repository directory not found: {root}"
            )

        dependencies = {}

        for file in self._get_python_files(root):
            relative_path = file.relative_to(root).as_posix()
            imports = set()

            try:
                source = file.read_text(
                    encoding="utf-8",
                    errors="ignore",
                )
                tree = ast.parse(source)

                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            imports.add(alias.name)

                    elif isinstance(node, ast.ImportFrom):
                        module_name = self._resolve_import(
                            node=node,
                            file_path=file,
                            root=root,
                        )

                        if module_name:
                            imports.add(module_name)

            except (SyntaxError, OSError, UnicodeError):
                # Skip files that cannot be parsed or read.
                continue

            dependencies[relative_path] = sorted(imports)

        return dependencies

    def analyze_detailed(self, repository_path: str) -> dict:
        """
        Return detailed import metadata for architecture analysis.

        Each file includes import names, import types, and line numbers.
        """
        root = Path(repository_path).resolve()

        if not root.is_dir():
            raise NotADirectoryError(
                f"Repository directory not found: {root}"
            )

        results = {}

        for file in self._get_python_files(root):
            relative_path = file.relative_to(root).as_posix()

            try:
                source = file.read_text(
                    encoding="utf-8",
                    errors="ignore",
                )
                tree = ast.parse(source)
            except (SyntaxError, OSError, UnicodeError):
                continue

            file_imports = []

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        file_imports.append({
                            "module": alias.name,
                            "import_type": "absolute",
                            "line": node.lineno,
                            "symbol": alias.asname,
                        })

                elif isinstance(node, ast.ImportFrom):
                    module_name = self._resolve_import(
                        node=node,
                        file_path=file,
                        root=root,
                    )

                    if module_name:
                        for alias in node.names:
                            file_imports.append({
                                "module": module_name,
                                "import_type": (
                                    "relative"
                                    if node.level > 0
                                    else "absolute"
                                ),
                                "line": node.lineno,
                                "symbol": alias.name,
                                "alias": alias.asname,
                            })

            results[relative_path] = {
                "imports": sorted(
                    file_imports,
                    key=lambda item: (
                        item["line"],
                        item["module"],
                        item.get("symbol", ""),
                    ),
                )
            }

        return results

    def _get_python_files(self, root: Path) -> list[Path]:
        """Collect Python files while excluding generated and environment folders."""
        files = []

        for file in root.rglob("*.py"):
            relative_path = file.relative_to(root)

            if any(
                part in self.IGNORE_DIRS
                for part in relative_path.parts
            ):
                continue

            files.append(file)

        return sorted(files)

    @staticmethod
    def _resolve_import(
        node: ast.ImportFrom,
        file_path: Path,
        root: Path,
    ) -> str:
        """
        Resolve relative imports into repository-style module names.

        Example:
        from .services import helper
        becomes package.services
        """
        module = node.module or ""

        if node.level == 0:
            return module

        relative_file = file_path.relative_to(root)
        package_parts = list(relative_file.parts[:-1])

        # A file named __init__.py represents its containing package.
        if file_path.name == "__init__.py":
            current_package = package_parts
        else:
            current_package = package_parts

        # level=1 means the current package; level=2 goes up one level.
        remove_count = node.level - 1

        if remove_count:
            current_package = current_package[:-remove_count]

        resolved_parts = current_package

        if module:
            resolved_parts = resolved_parts + module.split(".")

        return ".".join(part for part in resolved_parts if part)
