from app.services.knowledge_graph_service import KnowledgeGraphService

result = KnowledgeGraphService.build("app")

print()

print(result.keys())

print()

print("Graph Nodes :", len(result["graph"]["nodes"]))

print("Graph Edges :", len(result["graph"]["edges"]))

print("Python Files :", len(result["ast"]))

print("Import Relations :", len(result["imports"]))