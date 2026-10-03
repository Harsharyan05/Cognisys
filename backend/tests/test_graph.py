"""
Tests for the Code Graph.

Author: Harsh Aryan
Project: Cognisys
"""

from app.graph.graph_builder import GraphBuilder


def test_graph_builder_returns_graph():
    builder = GraphBuilder()

    graph = builder.build([])

    assert graph is not None
    assert hasattr(graph, "nodes")
    assert hasattr(graph, "edges")


def test_graph_starts_empty():
    builder = GraphBuilder()

    graph = builder.build([])

    assert len(graph.nodes) == 0
    assert len(graph.edges) == 0


def test_graph_nodes_are_dictionary():
    builder = GraphBuilder()

    relationships = [
        {
            "source": "app/service.py",
            "target": "app/repository.py",
            "type": "IMPORTS",
        }
    ]

    graph = builder.build(relationships)

    assert isinstance(graph.nodes, dict)

    assert "app/service.py" in graph.nodes
    assert "app/repository.py" in graph.nodes


def test_graph_edges_are_list():
    builder = GraphBuilder()

    relationships = [
        {
            "source": "app/service.py",
            "target": "app/repository.py",
            "type": "IMPORTS",
        }
    ]

    graph = builder.build(relationships)

    assert isinstance(graph.edges, list)

    assert len(graph.edges) == 1