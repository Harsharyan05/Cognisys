from app.parser.call_graph_builder import CallGraphBuilder

builder = CallGraphBuilder()

calls = builder.build("app")

print(f"\nTotal Calls: {len(calls)}\n")

for call in calls:
    print(call)