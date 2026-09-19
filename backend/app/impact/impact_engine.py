from typing import List, Optional

from app.impact.impact_analyzer import ImpactAnalyzer


class ImpactEngine:
    """
    Orchestrates architecture analysis and impact analysis.

    The engine obtains the dependency graph from the existing
    ArchitectureEngine and passes it to ImpactAnalyzer.
    """

    def __init__(self, architecture_engine):
        self.architecture_engine = architecture_engine

    def analyze(
        self,
        target: str,
        affected_apis: Optional[List[str]] = None,
        affected_services: Optional[List[str]] = None,
        affected_tests: Optional[List[str]] = None,
    ):
        """
        Analyze the impact of changing a repository module.
        """

        architecture_analysis = self.architecture_engine.analyze()

        dependency_graph = architecture_analysis.get(
            "dependency_graph",
            {},
        )

        analyzer = ImpactAnalyzer(dependency_graph)

        return analyzer.analyze(
            target=target,
            affected_apis=affected_apis,
            affected_services=affected_services,
            affected_tests=affected_tests,
        )