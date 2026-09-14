import json

from app.graph.graph_builder import GraphBuilder
from app.graph.graph_serializer import GraphSerializer

builder = GraphBuilder()

graph = builder.build(
    "storage/temp/Cognisys"
)

graph_json = GraphSerializer.serialize(graph)

print()

print(json.dumps(graph_json, indent=2))