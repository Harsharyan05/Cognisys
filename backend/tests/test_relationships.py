from app.graph.relationship_extractor import RelationshipExtractor

extractor = RelationshipExtractor()

edges = extractor.extract("storage/temp/Cognisys")

print(f"Total Edges: {len(edges)}")

print()

for edge in edges[:15]:
    print(edge)