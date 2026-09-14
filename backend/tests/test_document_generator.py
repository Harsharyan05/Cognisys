from app.architecture.architecture_engine import (
    ArchitectureEngine,
)

from app.ai.document_generator import (
    DocumentGenerator,
)


def main():

    engine = ArchitectureEngine(".")

    analysis = engine.analyze()

    generator = DocumentGenerator(".")

    document = generator.generate(
        analysis
    )

    print("\nRepository Document Generated")
    print("=" * 60)
    print(document)


if __name__ == "__main__":
    main()