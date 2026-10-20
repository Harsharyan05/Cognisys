
"""
Service Detector

Detects FastAPI applications, routers, and API endpoints.

Author: Harsh Aryan
Project: Cognisys
"""

import ast
from pathlib import Path
from typing import Dict, List, Optional


class ServiceDetector:
    """Detect FastAPI components inside a repository."""

    IGNORE_DIRS = {
        ".git",
        "__pycache__",
        ".venv",
        "venv",
        "node_modules",
        ".idea",
        ".vscode",
        ".pytest_cache",
        "storage",
    }

    def __init__(self, repository_path: str):
        self.repository_path = Path(repository_path).resolve()

    def detect(self) -> List[Dict]:
        services = []

        if not self.repository_path.is_dir():
            return services

        for file in self.repository_path.rglob("*.py"):
            if any(part in self.IGNORE_DIRS for part in file.parts):
                continue

            try:
                source = file.read_text(encoding="utf-8")
                tree = ast.parse(source)

                visitor = FastAPIVisitor(
                    file.relative_to(self.repository_path),
                    source,
                )
                visitor.visit(tree)
                services.extend(visitor.services)

            except (OSError, UnicodeDecodeError, SyntaxError, ValueError):
                # Continue scanning other files when one file cannot be parsed.
                continue

        return services


class FastAPIVisitor(ast.NodeVisitor):
    """Extract FastAPI app, router and route metadata."""

    HTTP_METHODS = {
        "get",
        "post",
        "put",
        "delete",
        "patch",
        "options",
        "head",
        "trace",
    }

    def __init__(self, file_path: Path, source: str = ""):
        self.file_path = str(file_path)
        self.source = source
        self.services: List[Dict] = []
        self.detected = set()

    @staticmethod
    def _call_name(node: ast.AST) -> Optional[str]:
        if isinstance(node, ast.Name):
            return node.id

        if isinstance(node, ast.Attribute):
            return node.attr

        return None

    @staticmethod
    def _literal_string(node: Optional[ast.AST]) -> Optional[str]:
        if node is None:
            return None

        try:
            value = ast.literal_eval(node)
        except (ValueError, TypeError):
            return None

        return value if isinstance(value, str) else None

    def _add_once(self, key: tuple, service: Dict) -> None:
        if key not in self.detected:
            self.detected.add(key)
            self.services.append(service)

    def visit_Assign(self, node: ast.Assign) -> None:
        if isinstance(node.value, ast.Call):
            name = self._call_name(node.value.func)

            if name in {"FastAPI", "APIRouter"}:
                component_type = (
                    "FastAPI Application"
                    if name == "FastAPI"
                    else "APIRouter"
                )

                for target in node.targets:
                    if isinstance(target, ast.Name):
                        variable_name = target.id

                        self._add_once(
                            (component_type, self.file_path, variable_name),
                            {
                                "type": component_type,
                                "name": variable_name,
                                "file": self.file_path,
                                "line": node.lineno,
                                "prefix": self._literal_string(
                                    next(
                                        (
                                            keyword.value
                                            for keyword in node.value.keywords
                                            if keyword.arg == "prefix"
                                        ),
                                        None,
                                    )
                                ) if name == "APIRouter" else None,
                            },
                        )

        self.generic_visit(node)

    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
        # Support annotated assignments such as:
        # app: FastAPI = FastAPI()
        if isinstance(node.value, ast.Call):
            name = self._call_name(node.value.func)

            if name in {"FastAPI", "APIRouter"} and isinstance(
                node.target, ast.Name
            ):
                component_type = (
                    "FastAPI Application"
                    if name == "FastAPI"
                    else "APIRouter"
                )

                variable_name = node.target.id
                self._add_once(
                    (component_type, self.file_path, variable_name),
                    {
                        "type": component_type,
                        "name": variable_name,
                        "file": self.file_path,
                        "line": node.lineno,
                        "prefix": self._literal_string(
                            next(
                                (
                                    keyword.value
                                    for keyword in node.value.keywords
                                    if keyword.arg == "prefix"
                                ),
                                None,
                            )
                        ) if name == "APIRouter" else None,
                    },
                )

        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._extract_routes(node)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._extract_routes(node)
        self.generic_visit(node)

    def _extract_routes(self, node) -> None:
        for decorator in node.decorator_list:
            if not isinstance(decorator, ast.Call):
                continue

            func = decorator.func
            method_name = self._call_name(func)

            if method_name not in self.HTTP_METHODS:
                continue

            # Avoid treating unrelated methods named get/post as API routes.
            if not isinstance(func, ast.Attribute):
                continue

            route_path = (
                self._literal_string(decorator.args[0])
                if decorator.args
                else None
            )

            route_owner = (
                func.value.id
                if isinstance(func.value, ast.Name)
                else None
            )

            service = {
                "type": "API Endpoint",
                "method": method_name.upper(),
                "function": node.name,
                "file": self.file_path,
                "line": node.lineno,
                "route": route_path,
                "router": route_owner,
                "is_async": isinstance(node, ast.AsyncFunctionDef),
            }

            # Include common FastAPI metadata where statically available.
            for keyword in decorator.keywords:
                if keyword.arg in {"name", "status_code", "summary", "deprecated"}:
                    try:
                        service[keyword.arg] = ast.literal_eval(keyword.value)
                    except (ValueError, TypeError):
                        pass

            key = (
                "API Endpoint",
                self.file_path,
                node.name,
                method_name.upper(),
                route_path,
                node.lineno,
            )
            self._add_once(key, service)
