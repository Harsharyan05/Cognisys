from pathlib import Path

from app.architecture.architecture_engine import (
    ArchitectureEngine,
)

from app.ai.knowledge_document_generator import (
    KnowledgeDocumentGenerator,
)


def main():

    engine = ArchitectureEngine(".")

    analysis = engine.analyze()

    generator = KnowledgeDocumentGenerator()

    generator.generate(
        analysis
    )

    print("\nGenerated Documents")
    print("=" * 60)

    for file in sorted(
        Path("storage/documents").glob("*.md")
    ):

        print(file.name)


if __name__ == "__main__":
    main()