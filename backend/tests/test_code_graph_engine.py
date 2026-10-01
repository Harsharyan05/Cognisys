from pathlib import Path

from app.graph.code_graph_engine import CodeGraphEngine


def create_repository(tmp_path: Path):
    (tmp_path / "service.py").write_text(
        """
def authenticate():
    find_user()

def find_user():
    pass
""",
        encoding="utf-8",
    )

    return tmp_path


def test_code_graph_engine_builds_graph(tmp_path):
    repository = create_repository(tmp_path)

    engine = CodeGraphEngine(
        repository_path=repository
    )

    graph = engine.build()

    assert graph is not None


def test_code_graph_engine_contains_nodes(tmp_path):
    repository = create_repository(tmp_path)

    engine = CodeGraphEngine(
        repository_path=repository
    )

    graph = engine.build()

    assert graph.has_node(
        "service.py:function:authenticate"
    )

    assert graph.has_node(
        "service.py:function:find_user"
    )


def test_code_graph_engine_contains_call_relationship(
    tmp_path,
):
    repository = create_repository(tmp_path)

    engine = CodeGraphEngine(
        repository_path=repository
    )

    graph = engine.build()

    assert graph.has_edge(
        "service.py:function:authenticate",
        "service.py:function:find_user",
        "CALLS",
    )


def test_code_graph_engine_uses_graph_builder(
    tmp_path,
):
    repository = create_repository(tmp_path)

    engine = CodeGraphEngine(
        repository_path=repository
    )

    graph = engine.build()

    assert len(graph.get_edges()) > 0