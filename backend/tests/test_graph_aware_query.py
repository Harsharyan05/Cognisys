from unittest.mock import MagicMock

from app.intelligence.graph_aware_query import (
    GraphAwareQuery,
)


def create_graph_query():
    graph_query = MagicMock()

    graph_query.get_callers.return_value = [
        "controller.py:method:AuthController.login"
    ]

    graph_query.get_callees.return_value = [
        "repository.py:method:UserRepository.find_user"
    ]

    graph_query.get_imports.return_value = [
        "app.database.users"
    ]

    graph_query.get_importers.return_value = [
        "app.services.users"
    ]

    graph_query.get_parent_classes.return_value = [
        "base.py:class:BaseService"
    ]

    graph_query.get_child_classes.return_value = [
        "auth.py:class:AdminService"
    ]

    graph_query.get_relationships.return_value = [
        {
            "source": (
                "service.py:method:"
                "AuthService.authenticate"
            ),
            "target": (
                "repository.py:method:"
                "UserRepository.find_user"
            ),
            "type": "CALLS",
        }
    ]

    return graph_query


def test_get_callers():
    graph_query = create_graph_query()

    query = GraphAwareQuery(
        graph_query
    )

    result = query.get_callers(
        "service.py:method:AuthService.authenticate"
    )

    assert result == [
        "controller.py:method:AuthController.login"
    ]


def test_get_callees():
    graph_query = create_graph_query()

    query = GraphAwareQuery(
        graph_query
    )

    result = query.get_callees(
        "service.py:method:AuthService.authenticate"
    )

    assert result == [
        "repository.py:method:UserRepository.find_user"
    ]


def test_get_imports():
    graph_query = create_graph_query()

    query = GraphAwareQuery(
        graph_query
    )

    result = query.get_imports(
        "app.services.users"
    )

    assert result == [
        "app.database.users"
    ]


def test_get_importers():
    graph_query = create_graph_query()

    query = GraphAwareQuery(
        graph_query
    )

    result = query.get_importers(
        "app.database.users"
    )

    assert result == [
        "app.services.users"
    ]


def test_get_parent_classes():
    graph_query = create_graph_query()

    query = GraphAwareQuery(
        graph_query
    )

    result = query.get_parent_classes(
        "auth.py:class:AdminService"
    )

    assert result == [
        "base.py:class:BaseService"
    ]


def test_get_child_classes():
    graph_query = create_graph_query()

    query = GraphAwareQuery(
        graph_query
    )

    result = query.get_child_classes(
        "base.py:class:BaseService"
    )

    assert result == [
        "auth.py:class:AdminService"
    ]


def test_get_relationships():
    graph_query = create_graph_query()

    query = GraphAwareQuery(
        graph_query
    )

    result = query.get_relationships(
        "service.py:method:AuthService.authenticate"
    )

    assert len(result) == 1
    assert result[0]["type"] == "CALLS"


def test_unknown_symbol_returns_empty():
    graph_query = MagicMock()

    graph_query.get_callers.return_value = []
    graph_query.get_callees.return_value = []
    graph_query.get_relationships.return_value = []

    query = GraphAwareQuery(
        graph_query
    )

    assert query.get_callers("unknown") == []
    assert query.get_callees("unknown") == []
    assert query.get_relationships("unknown") == []