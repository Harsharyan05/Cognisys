from app.parser.python_ast_parser import PythonASTParser

parser = PythonASTParser()

result = parser.parse("app")

print(f"\nPython files parsed: {len(result)}\n")

for file, data in result.items():
    print("=" * 60)
    print(file)
    print(data)