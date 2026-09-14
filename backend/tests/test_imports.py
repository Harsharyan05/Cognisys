from app.parser.import_graph_builder import ImportGraphBuilder

builder = ImportGraphBuilder()

relationships = builder.build("app")

print(f"\nTotal Import Relationships: {len(relationships)}\n")

for relation in relationships[:30]:

    print(relation)