from app.parser.call_graph_builder import CallGraphBuilder

builder = CallGraphBuilder()

calls = builder.build("app")

print()

print(f"Total Calls : {len(calls)}")

print()

for call in calls[:50]:

    print(call)