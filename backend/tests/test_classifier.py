from app.parser.file_classifier import FileClassifier

files = [
    "main.py",
    "repository_service.py",
    "analysis.py",
    "README.md",
    "Dockerfile",
    "requirements.txt",
]

for file in files:
    print(file, "->", FileClassifier.classify(file))