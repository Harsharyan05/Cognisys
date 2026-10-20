"""
Knowledge Document Generator

Generates multiple AI-readable knowledge documents.

Author: Harsh Aryan
Project: Cognisys
"""

from pathlib import Path
from typing import Dict

from app.architecture.service_detector import ServiceDetector
from app.architecture.dependency_graph import DependencyGraph
from app.parser.technology_detector import TechnologyDetector
from app.parser.repository_metadata import RepositoryMetadataAnalyzer
class KnowledgeDocumentGenerator:
    """
    Generates repository knowledge documents.
    """

    def __init__(
        self,
        output_directory: str = "storage/documents",
        repository_path: str = ".",
    ):

        self.output_directory = Path(output_directory)
        self.repository_path = Path(repository_path)
        self.output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    def generate(
        self,
        analysis: Dict,
    ):

        self._generate_architecture(analysis)
        self._generate_hotspots(analysis)
        self._generate_patterns(analysis)
        self._generate_recommendations(analysis)
        self._generate_services(analysis)
        self._generate_apis(analysis)
        self._generate_dependency_graph()
        self._generate_technologies()
        self._generate_repository_metadata()
        
        print("\nKnowledge documents generated successfully.")

    # ---------------------------------------------------------
    # Architecture
    # ---------------------------------------------------------

    def _generate_architecture(
        self,
        analysis: Dict,
    ):

        output = (
            self.output_directory /
            "architecture.md"
        )

        with open(
            output,
            "w",
            encoding="utf-8",
        ) as file:

            file.write("# Architecture\n\n")

            for layer, folders in analysis[
                "layers"
            ].items():

                file.write(
                    f"## {layer}\n\n"
                )

                for folder in folders:

                    file.write(
                        f"- {folder}\n"
                    )

                file.write("\n")
    # ---------------------------------------------------------
    # Services
    # ---------------------------------------------------------

    def _generate_services(
        self,
        analysis: Dict,
    ):

        services = self._discover_services()

        output = (
            self.output_directory /
            "services.md"
        )

        with open(
            output,
            "w",
            encoding="utf-8",
        ) as file:

            file.write("# Services\n\n")

            if not services:

                file.write(
                    "No services detected.\n"
                )

                return

            for service in services:

                file.write(
                    f"## {service['type']}\n\n"
                )

                for key, value in service.items():

                    if key == "type":
                        continue

                    file.write(
                        f"{key.title()} : {value}\n"
                    )

                file.write("\n")
    # ---------------------------------------------------------
    # APIs
    # ---------------------------------------------------------

    def _generate_apis(
        self,
        analysis: Dict,
    ):

        services = self._discover_services()

        output = (
            self.output_directory /
            "apis.md"
        )

        with open(
            output,
            "w",
            encoding="utf-8",
        ) as file:

            file.write("# API Endpoints\n\n")

            endpoints = [
                service
                for service in services
                if service["type"] == "API Endpoint"
            ]

            if not endpoints:

                file.write(
                    "No API endpoints detected.\n"
                )

                return

            
            for endpoint in endpoints:
                file.write(f"## {endpoint.get('method', 'UNKNOWN')} {endpoint.get('route') or '(route unresolved)'}\n\n")
                file.write(f"- Function: {endpoint.get('function', 'Unknown')}\n")
                file.write(f"- File: {endpoint.get('file', 'Unknown')}\n")

                if endpoint.get("line") is not None:
                    file.write(f"- Line: {endpoint['line']}\n")

                if endpoint.get("router"):
                    file.write(f"- Router: {endpoint['router']}\n")

                file.write("\n")
        
    # ---------------------------------------------------------
    # Hotspots
    # ---------------------------------------------------------

    def _generate_hotspots(
        self,
        analysis: Dict,
    ):

        output = (
            self.output_directory /
            "hotspots.md"
        )

        with open(
            output,
            "w",
            encoding="utf-8",
        ) as file:

            file.write(
                "# Repository Hotspots\n\n"
            )

            for hotspot in analysis[
                "hotspots"
            ]:

                file.write(
                    f"## {hotspot.module}\n\n"
                )

                file.write(
                    f"- Risk : {hotspot.risk}\n"
                )

                file.write(
                    f"- Fan In : {hotspot.fan_in}\n"
                )

                file.write(
                    f"- Fan Out : {hotspot.fan_out}\n"
                )

                file.write(
                    f"- Score : {hotspot.score}\n\n"
                )

    # ---------------------------------------------------------
    # Architecture Patterns
    # ---------------------------------------------------------

    def _generate_patterns(
        self,
        analysis: Dict,
    ):

        output = (
            self.output_directory /
            "architecture_patterns.md"
        )

        with open(
            output,
            "w",
            encoding="utf-8",
        ) as file:

            file.write(
                "# Architecture Patterns\n\n"
            )

            for pattern in analysis[
                "patterns"
            ]:

                file.write(
                    f"## {pattern.name}\n\n"
                )

                file.write(
                    f"Confidence : {pattern.confidence:.2f}\n\n"
                )

                file.write(
                    "Evidence\n\n"
                )

                for evidence in pattern.evidence:

                    file.write(
                        f"- {evidence}\n"
                    )

                file.write("\n")

    # ---------------------------------------------------------
    # Recommendations
    # ---------------------------------------------------------

    def _generate_recommendations(
        self,
        analysis: Dict,
    ):

        output = (
            self.output_directory /
            "recommendations.md"
        )

        with open(
            output,
            "w",
            encoding="utf-8",
        ) as file:

            file.write(
                "# Recommendations\n\n"
            )

            for recommendation in analysis[
                "recommendations"
            ]:

                file.write(
                    f"## {recommendation.title}\n\n"
                )

                file.write(
                    f"Priority : {recommendation.priority}\n\n"
                )

                file.write(
                    f"Module : {recommendation.module}\n\n"
                )

                file.write(
                    recommendation.recommendation
                )

                file.write("\n\n")
                
    # ---------------------------------------------------------
    # Dependency Graph
    # ---------------------------------------------------------

    def _generate_dependency_graph(self):
        """Generate dependency graph documentation."""

        graph = DependencyGraph(
            str(self.repository_path.resolve())
        ).build()

        output = self.output_directory / "dependency_graph.md"

        with open(output, "w", encoding="utf-8") as file:
            file.write("# Dependency Graph\n\n")
            file.write(
                "This document contains the module dependency graph "
                "generated from the repository.\n\n"
            )

            total_modules = len(graph)
            total_dependencies = sum(
                len(dependencies)
                for dependencies in graph.values()
            )

            file.write("## Summary\n\n")
            file.write(f"- Total Modules: {total_modules}\n")
            file.write(
                f"- Total Dependencies: {total_dependencies}\n\n"
            )
            file.write("---\n\n")

            for module in sorted(graph):
                dependencies = sorted(graph[module])

                file.write(f"## {module}\n\n")
                file.write(
                    f"Dependency Count: {len(dependencies)}\n\n"
                )

                if dependencies:
                    file.write("### Imports\n\n")

                    for dependency in dependencies:
                        file.write(f"- {dependency}\n")
                else:
                    file.write("No imported modules.\n")

                file.write("\n---\n\n")

    # ---------------------------------------------------------
    # Technologies
    # ---------------------------------------------------------

    def _generate_technologies(self):
        """Generate technology documentation."""

        repository_root = self.repository_path.resolve()
        detector = TechnologyDetector()
        technologies = detector.detect(repository_root)

        output = self.output_directory / "technologies.md"

        with open(output, "w", encoding="utf-8") as file:
            file.write("# Technologies\n\n")

            if not technologies:
                file.write("No technologies detected.\n")
                return

            for category, items in technologies.items():
                title = category.replace("_", " ").title()
                file.write(f"## {title}\n\n")

                if items:
                    for item in items:
                        file.write(f"- {item}\n")
                else:
                    file.write("None detected.\n")

                file.write("\n")
    
    
    def _generate_repository_metadata(self):
        """Generate a Markdown summary of repository metadata."""
        analyzer = RepositoryMetadataAnalyzer(
            str(self.repository_path.resolve())
        )
        metadata = analyzer.analyze()

        output_path = (
            self.output_directory / "repository_metadata.md"
        )

        with output_path.open("w", encoding="utf-8") as file:
            file.write("# Repository Metadata\n\n")
            file.write(
                f"- **Repository:** {metadata['repository_name']}\n"
            )
            file.write(
                f"- **Root:** {metadata['repository_root']}\n"
            )
            file.write(
                f"- **Total files:** {metadata['total_files']}\n\n"
            )

            file.write("## Language Distribution\n\n")
            if metadata["language_counts"]:
                for language, count in metadata["language_counts"].items():
                    file.write(f"- {language}: {count} files\n")
            else:
                file.write("- No recognized languages detected.\n")

            file.write("\n## File Extensions\n\n")
            for extension, count in metadata["extension_counts"].items():
                file.write(f"- `{extension}`: {count} files\n")

            file.write("\n## Directory Distribution\n\n")
            for directory, count in metadata["directory_file_counts"].items():
                file.write(f"- `{directory}`: {count} files\n")

            file.write("\n## Project Configuration Files\n\n")
            if metadata["project_files"]:
                for project_file in metadata["project_files"]:
                    file.write(f"- `{project_file}`\n")
            else:
                file.write("- No recognized project files detected.\n")
            