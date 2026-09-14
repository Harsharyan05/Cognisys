"""
Repository Overview Generator Test

Author: Harsh Aryan
Project: Cognisys
"""

from app.ai.repository_overview_generator import (
    RepositoryOverviewGenerator,
)


def main():

    generator = RepositoryOverviewGenerator()

    print("=" * 80)
    print("Repository Overview Generator")
    print("=" * 80)

    overview = generator.generate()

    print("\nGenerated Overview\n")
    print("=" * 80)
    print(overview)

    output = generator.save()

    print("\n")
    print("=" * 80)
    print("Overview saved successfully.")
    print(f"Location : {output}")
    print("=" * 80)


if __name__ == "__main__":
    main()