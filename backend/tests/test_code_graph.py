from app.graph.code_graph import CodeGraph


def test_add_node():
    graph = CodeGraph()

    graph.add_node(
        "app.py:function:main",
        node_type="function",
    )

    assert graph.has_node(
        "app.py:function:main"
    )


def test_add_edge():
    graph = CodeGraph()

    graph.add_node(
        "a.py:function:foo",
        node_type="function",
    )
    graph.add_node(
        "b.py:function:bar",
        node_type="function",
    )

    graph.add_edge(
        "a.py:function:foo",
        "b.py:function:bar",
        relationship_type="CALLS",
    )

    assert graph.has_edge(
        "a.py:function:foo",
        "b.py:function:bar",
        relationship_type="CALLS",
    )


def test_get_callees():
    graph = CodeGraph()

    graph.add_edge(
        "a.py:function:foo",
        "b.py:function:bar",
        relationship_type="CALLS",
    )

    graph.add_edge(
        "a.py:function:foo",
        "c.py:function:baz",
        relationship_type="CALLS",
    )

    assert set(
        graph.get_callees(
            "a.py:function:foo"
        )
    ) == {
        "b.py:function:bar",
        "c.py:function:baz",
    }


def test_get_callers():
    graph = CodeGraph()

    graph.add_edge(
        "a.py:function:foo",
        "b.py:function:bar",
        relationship_type="CALLS",
    )

    graph.add_edge(
        "c.py:function:baz",
        "b.py:function:bar",
        relationship_type="CALLS",
    )

    assert set(
        graph.get_callers(
            "b.py:function:bar"
        )
    ) == {
        "a.py:function:foo",
        "c.py:function:baz",
    }


def test_get_imports():
    graph = CodeGraph()

    graph.add_edge(
        "services.py",
        "repositories.py",
        relationship_type="IMPORTS",
    )

    assert graph.get_imports(
        "services.py"
    ) == [
        "repositories.py"
    ]


def test_get_importers():
    graph = CodeGraph()

    graph.add_edge(
        "services.py",
        "repositories.py",
        relationship_type="IMPORTS",
    )

    assert graph.get_importers(
        "repositories.py"
    ) == [
        "services.py"
    ]


def test_get_parent_classes():
    graph = CodeGraph()

    graph.add_edge(
        "auth.py:class:AdminService",
        "base.py:class:BaseService",
        relationship_type="INHERITS",
    )

    assert graph.get_parent_classes(
        "auth.py:class:AdminService"
    ) == [
        "base.py:class:BaseService"
    ]


def test_get_child_classes():
    graph = CodeGraph()

    graph.add_edge(
        "auth.py:class:AdminService",
        "base.py:class:BaseService",
        relationship_type="INHERITS",
    )

    assert graph.get_child_classes(
        "base.py:class:BaseService"
    ) == [
        "auth.py:class:AdminService"
    ]