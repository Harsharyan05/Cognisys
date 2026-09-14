from app.graph.entity_extractor import EntityExtractor

extractor = EntityExtractor()

nodes = extractor.extract("storage/temp/Cognisys")

print()

print(f"Total Nodes: {len(nodes)}")

print()

for node in nodes[:10]:
    print(node)