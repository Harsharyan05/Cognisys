"""
Architecture Citation Engine

Converts structured architecture analysis into
stable, machine-readable citations.

Author: Harsh Aryan
Project: Cognisys
"""

from typing import Any, Dict, List


class ArchitectureCitationEngine:
    """
    Generates citations for structured architecture facts.

    Supported citation types:
    - architecture_layer
    - architecture_dependency
    - architecture_cycle
    - architecture_hotspot
    - architecture_pattern
    - architecture_recommendation
    """

    def __init__(self, analysis: Dict[str, Any]):
        self.analysis = analysis or {}

    def generate(self) -> List[Dict[str, Any]]:
        """
        Generate all architecture citations.
        """

        citations = []

        citations.extend(
            self._generate_layer_citations()
        )

        citations.extend(
            self._generate_dependency_citations()
        )

        citations.extend(
            self._generate_cycle_citations()
        )

        citations.extend(
            self._generate_hotspot_citations()
        )

        citations.extend(
            self._generate_pattern_citations()
        )

        citations.extend(
            self._generate_recommendation_citations()
        )

        return citations

    # ---------------------------------------------------------
    # Layers
    # ---------------------------------------------------------

    def _generate_layer_citations(self):
        citations = []

        layers = self.analysis.get(
            "layers",
            {},
        )

        for layer, modules in layers.items():

            citation_id = (
                f"ARCH-LAYER-{len(citations) + 1:03d}"
            )

            citations.append(
                {
                    "id": citation_id,
                    "type": "architecture_layer",
                    "source": {
                        "layer": layer,
                        "modules": modules,
                    },
                    "content": (
                        f"{layer} layer contains "
                        f"{len(modules)} module group(s)."
                    ),
                }
            )

        return citations

    # ---------------------------------------------------------
    # Dependencies
    # ---------------------------------------------------------

    def _generate_dependency_citations(self):
        citations = []

        dependency_graph = self.analysis.get(
            "dependency_graph",
            {},
        )

        for module, dependencies in dependency_graph.items():

            citation_id = (
                f"ARCH-DEP-{len(citations) + 1:03d}"
            )

            citations.append(
                {
                    "id": citation_id,
                    "type": "architecture_dependency",
                    "source": {
                        "module": module,
                        "dependencies": dependencies,
                    },
                    "content": (
                        f"{module} depends on "
                        f"{', '.join(dependencies) if dependencies else 'no modules'}."
                    ),
                }
            )

        return citations

    # ---------------------------------------------------------
    # Circular Dependencies
    # ---------------------------------------------------------

    def _generate_cycle_citations(self):
        citations = []

        cycles = self.analysis.get(
            "cycles",
            [],
        )

        for index, cycle in enumerate(cycles, start=1):

            citation_id = (
                f"ARCH-CYCLE-{index:03d}"
            )

            citations.append(
                {
                    "id": citation_id,
                    "type": "architecture_cycle",
                    "source": {
                        "cycle": cycle,
                    },
                    "content": (
                        "Circular dependency detected: "
                        + " -> ".join(cycle)
                    ),
                }
            )

        return citations

    # ---------------------------------------------------------
    # Hotspots
    # ---------------------------------------------------------

    def _generate_hotspot_citations(self):
        citations = []

        hotspots = self.analysis.get(
            "hotspots",
            [],
        )

        for index, hotspot in enumerate(
            hotspots,
            start=1,
        ):

            if hasattr(hotspot, "__dict__"):
                hotspot = hotspot.__dict__

            citation_id = (
                f"ARCH-HOTSPOT-{index:03d}"
            )

            citations.append(
                {
                    "id": citation_id,
                    "type": "architecture_hotspot",
                    "source": hotspot,
                    "content": (
                        f"Architecture hotspot: "
                        f"{hotspot.get('module', 'unknown')} "
                        f"with risk "
                        f"{hotspot.get('risk', 'UNKNOWN')}."
                    ),
                }
            )

        return citations

    # ---------------------------------------------------------
    # Patterns
    # ---------------------------------------------------------

    def _generate_pattern_citations(self):
        citations = []

        patterns = self.analysis.get(
            "patterns",
            [],
        )

        for index, pattern in enumerate(
            patterns,
            start=1,
        ):

            if hasattr(pattern, "__dict__"):
                pattern = pattern.__dict__

            citation_id = (
                f"ARCH-PATTERN-{index:03d}"
            )

            pattern_name = pattern.get(
                "pattern",
                pattern.get(
                    "name",
                    "Unknown",
                ),
            )

            citations.append(
                {
                    "id": citation_id,
                    "type": "architecture_pattern",
                    "source": pattern,
                    "content": (
                        f"Architecture pattern detected: "
                        f"{pattern_name}."
                    ),
                }
            )

        return citations

    # ---------------------------------------------------------
    # Recommendations
    # ---------------------------------------------------------

    def _generate_recommendation_citations(self):
        citations = []

        recommendations = self.analysis.get(
            "recommendations",
            [],
        )

        for index, recommendation in enumerate(
            recommendations,
            start=1,
        ):

            if hasattr(
                recommendation,
                "__dict__",
            ):
                recommendation = (
                    recommendation.__dict__
                )

            citation_id = (
                f"ARCH-RECOMMENDATION-{index:03d}"
            )

            message = recommendation.get(
                "message",
                recommendation.get(
                    "recommendation",
                    "",
                ),
            )

            citations.append(
                {
                    "id": citation_id,
                    "type": (
                        "architecture_recommendation"
                    ),
                    "source": recommendation,
                    "content": message,
                }
            )

        return citations