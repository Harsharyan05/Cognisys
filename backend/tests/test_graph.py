from app.graph.graph_builder import GraphBuilder

builder = GraphBuilder()

graph = builder.build(
    "storage/temp/Cognisys"
)

print()

print("Nodes :", len(graph.nodes))
print("Edges :", len(graph.edges))

print()

print(graph.nodes[:5])

print()

print(graph.edges[:5])