import sys
from pathlib import Path

# Add backend directory to Python path
BACKEND_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_DIR))

from app.architecture.architecture_engine import ArchitectureEngine


def main():
    engine = ArchitectureEngine(
        repository_path=str(BACKEND_DIR),
        output_directory=str(BACKEND_DIR / "reports"),
    )

    result = engine.analyze()

    print("\n")
    print("=" * 70)
    print("COGNISYS ARCHITECTURE ANALYSIS")
    print("=" * 70)

    print("\nLayers")
    print("-" * 70)

    for layer, directories in result["layers"].items():
        print(f"{layer}: {directories}")

    print("\nDependency Graph")
    print("-" * 70)
    print(f"Modules: {len(result['dependency_graph'])}")

    for module, dependencies in result["dependency_graph"].items():
        print(f"{module} -> {dependencies}")

    print("\nCircular Dependencies")
    print("-" * 70)

    if result["cycles"]:
        for cycle in result["cycles"]:
            print(" -> ".join(cycle))
    else:
        print("No circular dependencies detected.")

    print("\nHotspots")
    print("-" * 70)

    if result["hotspots"]:
        for hotspot in result["hotspots"]:
            print(
                f"{hotspot.module} | "
                f"Fan-in: {hotspot.fan_in} | "
                f"Fan-out: {hotspot.fan_out} | "
                f"Score: {hotspot.score} | "
                f"Risk: {hotspot.risk}"
            )
    else:
        print("No hotspots detected.")

    print("\nArchitecture Patterns")
    print("-" * 70)

    if result["patterns"]:
        for pattern in result["patterns"]:
            print(
                f"{pattern.name} | "
                f"Confidence: {pattern.confidence:.2f}"
            )

            for evidence in pattern.evidence:
                print(f"  - {evidence}")
    else:
        print("No architecture patterns detected.")

    print("\nRecommendations")
    print("-" * 70)

    if result["recommendations"]:
        for recommendation in result["recommendations"]:
            print(
                f"[{recommendation.priority}] "
                f"{recommendation.title} | "
                f"{recommendation.module}"
            )
            print(
                f"  {recommendation.recommendation}"
            )
    else:
        print("No recommendations.")

    print("\nReports")
    print("-" * 70)
    print(f"JSON     : {result['json_report']}")
    print(f"Markdown : {result['markdown_report']}")

    print("\n")
    print("=" * 70)
    print("ARCHITECTURE ANALYSIS COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()