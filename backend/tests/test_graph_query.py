from app.graph.code_graph import CodeGraph
from app.graph.graph_query import GraphQuery


def create_graph():
    graph = CodeGraph()

    graph.add_edge(
        "controller.py:method:AuthController.login",
        "service.py:method:AuthService.authenticate",
        relationship_type="CALLS",
    )

    graph.add_edge(
        "service.py:method:AuthService.authenticate",
        "repository.py:method:UserRepository.find_user",
        relationship_type="CALLS",
    )

    graph.add_edge(
        "service.py",
        "repository.py",
        relationship_type="IMPORTS",
    )

    graph.add_edge(
        "auth.py:class:AdminService",
        "base.py:class:BaseService",
        relationship_type="INHERITS",
    )

    return graph


def test_get_callers():
    graph = create_graph()
    query = GraphQuery(graph)

    result = query.get_callers(
        "service.py:method:AuthService.authenticate"
    )

    assert result == [
        "controller.py:method:AuthController.login"
    ]


def test_get_callees():
    graph = create_graph()
    query = GraphQuery(graph)

    result = query.get_callees(
        "service.py:method:AuthService.authenticate"
    )

    assert result == [
        "repository.py:method:UserRepository.find_user"
    ]


def test_get_imports():
    graph = create_graph()
    query = GraphQuery(graph)

    result = query.get_imports(
        "service.py"
    )

    assert result == [
        "repository.py"
    ]


def test_get_importers():
    graph = create_graph()
    query = GraphQuery(graph)

    result = query.get_importers(
        "repository.py"
    )

    assert result == [
        "service.py"
    ]


def test_get_parent_classes():
    graph = create_graph()
    query = GraphQuery(graph)

    result = query.get_parent_classes(
        "auth.py:class:AdminService"
    )

    assert result == [
        "base.py:class:BaseService"
    ]


def test_get_child_classes():
    graph = create_graph()
    query = GraphQuery(graph)

    result = query.get_child_classes(
        "base.py:class:BaseService"
    )

    assert result == [
        "auth.py:class:AdminService"
    ]


def test_get_all_relationships():
    graph = create_graph()
    query = GraphQuery(graph)

    result = query.get_relationships(
        "service.py:method:AuthService.authenticate"
    )

    assert len(result) == 2


def test_unknown_symbol_returns_empty():
    graph = create_graph()
    query = GraphQuery(graph)

    assert (
        query.get_callers("unknown")
        == []
    )

    assert (
        query.get_callees("unknown")
        == []
    )