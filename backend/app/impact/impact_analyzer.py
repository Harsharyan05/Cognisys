from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class ImpactResult:
    target: str
    direct_dependents: List[str]
    indirect_dependents: List[str]
    affected_apis: List[str] = field(default_factory=list)
    affected_services: List[str] = field(default_factory=list)
    affected_tests: List[str] = field(default_factory=list)
    risk: str = "LOW"


class ImpactAnalyzer:
    """
    Analyzes the impact of changing a module based on
    the repository dependency graph.
    """

    def __init__(self, dependency_graph: Dict[str, List[str]]):
        self.dependency_graph = dependency_graph

    def analyze(
        self,
        target: str,
        affected_apis: Optional[List[str]] = None,
        affected_services: Optional[List[str]] = None,
        affected_tests: Optional[List[str]] = None,
    ) -> ImpactResult:

        direct_dependents = self._find_direct_dependents(target)

        indirect_dependents = self._find_indirect_dependents(
            target,
            direct_dependents,
        )

        affected_apis = sorted(affected_apis or [])
        affected_services = sorted(affected_services or [])
        affected_tests = sorted(affected_tests or [])

        risk = self._calculate_risk(
            target=target,
            direct_dependents=direct_dependents,
            indirect_dependents=indirect_dependents,
            affected_apis=affected_apis,
            affected_services=affected_services,
            affected_tests=affected_tests,
        )

        return ImpactResult(
            target=target,
            direct_dependents=sorted(direct_dependents),
            indirect_dependents=sorted(indirect_dependents),
            affected_apis=affected_apis,
            affected_services=affected_services,
            affected_tests=affected_tests,
            risk=risk,
        )

    def _find_direct_dependents(self, target: str) -> List[str]:
        """
        Find modules that directly depend on the target.
        """
        dependents = []

        for module, dependencies in self.dependency_graph.items():
            if target in dependencies:
                dependents.append(module)

        return dependents

    def _find_indirect_dependents(
        self,
        target: str,
        direct_dependents: List[str],
    ) -> List[str]:
        """
        Find modules that depend on the target indirectly.

        Uses backwards traversal and prevents infinite loops
        caused by circular dependencies.
        """
        indirect = set()
        visited = set(direct_dependents)
        queue = list(direct_dependents)

        while queue:
            current = queue.pop(0)

            for module, dependencies in self.dependency_graph.items():
                if (
                    current in dependencies
                    and module not in visited
                    and module != target
                ):
                    visited.add(module)
                    indirect.add(module)
                    queue.append(module)

        return list(indirect)

    def _calculate_risk(
        self,
        target: str,
        direct_dependents: List[str],
        indirect_dependents: List[str],
        affected_apis: List[str],
        affected_services: List[str],
        affected_tests: List[str],
    ) -> str:
        """
        Calculate impact risk using transparent deterministic rules.
        """

        total_dependents = len(direct_dependents) + len(
            indirect_dependents
        )

        # Circular dependency involving the target.
        if self._has_circular_dependency(target):
            return "HIGH"

        # API exposed with multiple downstream dependents.
        if affected_apis and total_dependents >= 3:
            return "HIGH"

        # Large dependency impact.
        if total_dependents >= 6:
            return "HIGH"

        # Moderate dependency impact.
        if total_dependents >= 3:
            return "MEDIUM"

        # API/service/test combination with meaningful impact.
        if (
            affected_apis
            and affected_services
            and total_dependents >= 2
        ):
            return "HIGH"

        # Small or isolated changes.
        return "LOW"

    def _has_circular_dependency(self, target: str) -> bool:
        """
        Determine whether the target participates in a dependency cycle.
        """

        direct_dependents = self._find_direct_dependents(target)

        visited = set()
        queue = list(direct_dependents)

        while queue:
            current = queue.pop(0)

            if current == target:
                return True

            if current in visited:
                continue

            visited.add(current)

            for module, dependencies in self.dependency_graph.items():
                if current in dependencies:
                    queue.append(module)

        return False