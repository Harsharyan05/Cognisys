from app.graph.code_graph import CodeGraph
from app.graph.graph_builder import GraphBuilder


def test_builds_graph_from_relationships():
    relationships = [
        {
            "source": "auth.py:function:login",
            "target": "auth.py:function:authenticate",
            "type": "CALLS",
        },
        {
            "source": "auth.py:function:authenticate",
            "target": "user.py:function:find_user",
            "type": "CALLS",
        },
    ]

    builder = GraphBuilder()

    graph = builder.build(relationships)

    assert isinstance(graph, CodeGraph)

    assert graph.has_node(
        "auth.py:function:login"
    )

    assert graph.has_node(
        "auth.py:function:authenticate"
    )

    assert graph.has_node(
        "user.py:function:find_user"
    )


def test_builds_call_edges():
    relationships = [
        {
            "source": "auth.py:function:login",
            "target": "auth.py:function:authenticate",
            "type": "CALLS",
        },
    ]

    builder = GraphBuilder()

    graph = builder.build(relationships)

    assert graph.has_edge(
        "auth.py:function:login",
        "auth.py:function:authenticate",
        relationship_type="CALLS",
    )


def test_builds_import_edges():
    relationships = [
        {
            "source": "services.py",
            "target": "repositories.py",
            "type": "IMPORTS",
        },
    ]

    builder = GraphBuilder()

    graph = builder.build(relationships)

    assert graph.has_edge(
        "services.py",
        "repositories.py",
        relationship_type="IMPORTS",
    )


def test_builds_inheritance_edges():
    relationships = [
        {
            "source": "auth.py:class:AdminService",
            "target": "base.py:class:BaseService",
            "type": "INHERITS",
        },
    ]

    builder = GraphBuilder()

    graph = builder.build(relationships)

    assert graph.has_edge(
        "auth.py:class:AdminService",
        "base.py:class:BaseService",
        relationship_type="INHERITS",
    )


def test_builds_reverse_relationships():
    relationships = [
        {
            "source": "auth.py:function:login",
            "target": "auth.py:function:authenticate",
            "type": "CALLS",
        },
        {
            "source": "auth.py:function:authenticate",
            "target": "auth.py:function:login",
            "type": "CALLED_BY",
        },
    ]

    builder = GraphBuilder()

    graph = builder.build(relationships)

    assert graph.has_edge(
        "auth.py:function:authenticate",
        "auth.py:function:login",
        relationship_type="CALLED_BY",
    )


def test_empty_relationships_create_empty_graph():
    builder = GraphBuilder()

    graph = builder.build([])

    assert isinstance(graph, CodeGraph)
    assert graph.get_nodes() == []
    assert graph.get_edges() == []


def test_duplicate_relationships_are_not_duplicated():
    relationships = [
        {
            "source": "a.py:function:foo",
            "target": "b.py:function:bar",
            "type": "CALLS",
        },
        {
            "source": "a.py:function:foo",
            "target": "b.py:function:bar",
            "type": "CALLS",
        },
    ]

    builder = GraphBuilder()

    graph = builder.build(relationships)

    assert len(graph.get_edges()) == 1