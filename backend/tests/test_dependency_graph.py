from pathlib import Path

from app.architecture.dependency_graph import (
    DependencyGraph,
    ImportVisitor,
)


def test_dependency_graph_initialization(tmp_path):
    graph = DependencyGraph(str(tmp_path))

    assert graph.repository_path == Path(tmp_path)


def test_get_module_name(tmp_path):
    graph = DependencyGraph(str(tmp_path))

    file = tmp_path / "app" / "parser" / "python_ast_parser.py"
    file.parent.mkdir(parents=True)
    file.touch()

    result = graph.get_module_name(file)

    assert result == "app.parser.python_ast_parser"


def test_import_visitor_import():
    source = """
import os
import sys
import numpy
"""

    import ast

    tree = ast.parse(source)

    visitor = ImportVisitor()
    visitor.visit(tree)

    assert visitor.imports == {
        "os",
        "sys",
        "numpy",
    }


def test_import_visitor_import_from():
    source = """
from pathlib import Path
from typing import List
from app.ai.rag_pipeline import RAGPipeline
"""

    import ast

    tree = ast.parse(source)

    visitor = ImportVisitor()
    visitor.visit(tree)

    assert visitor.imports == {
        "pathlib",
        "typing",
        "app.ai.rag_pipeline",
    }


def test_import_visitor_mixed_imports():
    source = """
import os
import json
from pathlib import Path
from app.ai import rag_pipeline
"""

    import ast

    tree = ast.parse(source)

    visitor = ImportVisitor()
    visitor.visit(tree)

    assert visitor.imports == {
        "os",
        "json",
        "pathlib",
        "app.ai",
    }


def test_build_dependency_graph(tmp_path):
    app_dir = tmp_path / "app"
    app_dir.mkdir()

    main_file = app_dir / "main.py"

    main_file.write_text(
        """
import os
import json
from pathlib import Path
""",
        encoding="utf-8",
    )

    graph = DependencyGraph(str(tmp_path)).build()

    assert "app.main" in graph

    assert graph["app.main"] == [
        "json",
        "os",
        "pathlib",
    ]


def test_build_multiple_modules(tmp_path):
    app_dir = tmp_path / "app"
    app_dir.mkdir()

    (app_dir / "main.py").write_text(
        "from app.services import Service\n",
        encoding="utf-8",
    )

    (app_dir / "services.py").write_text(
        "import os\n",
        encoding="utf-8",
    )

    graph = DependencyGraph(str(tmp_path)).build()

    assert "app.main" in graph
    assert "app.services" in graph

    assert graph["app.main"] == ["app.services"]
    assert graph["app.services"] == ["os"]


def test_dependencies_are_sorted(tmp_path):
    app_dir = tmp_path / "app"
    app_dir.mkdir()

    (app_dir / "main.py").write_text(
        """
import zlib
import os
import json
import sys
""",
        encoding="utf-8",
    )

    graph = DependencyGraph(str(tmp_path)).build()

    assert graph["app.main"] == [
        "json",
        "os",
        "sys",
        "zlib",
    ]


def test_test_files_are_ignored(tmp_path):
    app_dir = tmp_path / "app"
    app_dir.mkdir()

    (app_dir / "main.py").write_text(
        "import os\n",
        encoding="utf-8",
    )

    (app_dir / "test_example.py").write_text(
        "import pytest\n",
        encoding="utf-8",
    )

    graph = DependencyGraph(str(tmp_path)).build()

    assert "app.main" in graph
    assert "app.test_example" not in graph


def test_tests_directory_is_ignored(tmp_path):
    app_dir = tmp_path / "app"
    tests_dir = tmp_path / "tests"

    app_dir.mkdir()
    tests_dir.mkdir()

    (app_dir / "main.py").write_text(
        "import os\n",
        encoding="utf-8",
    )

    (tests_dir / "test_main.py").write_text(
        "import pytest\n",
        encoding="utf-8",
    )

    graph = DependencyGraph(str(tmp_path)).build()

    assert "app.main" in graph
    assert all(
        not module.startswith("tests.")
        for module in graph
    )


def test_invalid_python_file_does_not_crash(tmp_path):
    app_dir = tmp_path / "app"
    app_dir.mkdir()

    (app_dir / "broken.py").write_text(
        "this is not valid python !!!",
        encoding="utf-8",
    )

    graph = DependencyGraph(str(tmp_path)).build()

    assert "app.broken" in graph
    assert graph["app.broken"] == []


def test_file_with_no_imports(tmp_path):
    app_dir = tmp_path / "app"
    app_dir.mkdir()

    (app_dir / "simple.py").write_text(
        """
def hello():
    return "Hello"
""",
        encoding="utf-8",
    )

    graph = DependencyGraph(str(tmp_path)).build()

    assert "app.simple" in graph
    assert graph["app.simple"] == []


def test_nested_module(tmp_path):
    nested_dir = (
        tmp_path
        / "app"
        / "api"
        / "v1"
    )

    nested_dir.mkdir(parents=True)

    file = nested_dir / "repository.py"

    file.write_text(
        "import os\n",
        encoding="utf-8",
    )

    graph = DependencyGraph(str(tmp_path)).build()

    assert "app.api.v1.repository" in graph
    assert graph["app.api.v1.repository"] == ["os"]