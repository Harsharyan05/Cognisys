class ArchitectureAwareRetriever:
    """
    Selects architecture context relevant to a repository question.

    This layer does not perform semantic/vector retrieval.
    It filters the structured architecture analysis into
    question-specific textual context for the intelligence layer.
    """

    def __init__(self, architecture):
        self.architecture = architecture or {}

    def retrieve(self, question: str):
        question_lower = question.lower().strip()

        # More specific architecture concepts must be checked
        # before generic dependency matching.
        if self._is_cycle_query(question_lower):
            return {
                "category": "CYCLE",
                "context": self._cycle_context(),
            }

        if self._is_dependency_query(question_lower):
            return {
                "category": "DEPENDENCY",
                "context": self._dependency_context(),
            }

        if self._is_hotspot_query(question_lower):
            return {
                "category": "HOTSPOT",
                "context": self._hotspot_context(),
            }

        if self._is_pattern_query(question_lower):
            return {
                "category": "PATTERN",
                "context": self._pattern_context(),
            }

        if self._is_risk_query(question_lower):
            return {
                "category": "RISK",
                "context": self._risk_context(),
            }

        return {
            "category": "GENERAL",
            "context": self._general_context(),
        }

    # ---------------------------------------------------------
    # Query classification
    # ---------------------------------------------------------

    @staticmethod
    def _is_dependency_query(question: str) -> bool:
        keywords = (
            "depend",
            "dependency",
            "dependencies",
        )
        return any(keyword in question for keyword in keywords)

    @staticmethod
    def _is_hotspot_query(question: str) -> bool:
        keywords = (
            "hotspot",
            "hotspots",
            "coupling",
        )
        return any(keyword in question for keyword in keywords)

    @staticmethod
    def _is_cycle_query(question: str) -> bool:
        keywords = (
            "circular",
            "cycle",
            "cycles",
        )
        return any(keyword in question for keyword in keywords)

    @staticmethod
    def _is_pattern_query(question: str) -> bool:
        keywords = (
            "pattern",
            "patterns",
        )
        return any(keyword in question for keyword in keywords)

    @staticmethod
    def _is_risk_query(question: str) -> bool:
        keywords = (
            "risk",
            "risks",
        )
        return any(keyword in question for keyword in keywords)

    # ---------------------------------------------------------
    # Context builders
    # ---------------------------------------------------------

    def _dependency_context(self):
        dependency_graph = self.architecture.get(
            "dependency_graph",
            {},
        )

        lines = []

        for module, dependencies in dependency_graph.items():
            lines.append(
                f"{module} depends on: "
                f"{', '.join(dependencies) if dependencies else 'none'}"
            )

        return "\n".join(lines)

    def _hotspot_context(self):
        hotspots = self.architecture.get(
            "hotspots",
            [],
        )

        lines = []

        for hotspot in hotspots:
            lines.append(
                f"{hotspot.get('module')}: "
                f"fan_in={hotspot.get('fan_in')}, "
                f"fan_out={hotspot.get('fan_out')}, "
                f"score={hotspot.get('score')}, "
                f"risk={hotspot.get('risk')}"
            )

        return "\n".join(lines)

    def _cycle_context(self):
        cycles = self.architecture.get(
            "cycles",
            [],
        )

        lines = []

        for cycle in cycles:
            lines.append(
                " -> ".join(cycle)
            )

        return "\n".join(lines)

    def _pattern_context(self):
        patterns = self.architecture.get(
            "patterns",
            [],
        )

        lines = []

        for pattern in patterns:
            lines.append(
                f"{pattern.get('pattern')}: "
                f"confidence={pattern.get('confidence')}"
            )

        return "\n".join(lines)

    def _risk_context(self):
        recommendations = self.architecture.get(
            "recommendations",
            [],
        )

        lines = []

        for recommendation in recommendations:
            lines.append(
                f"{recommendation.get('title')}: "
                f"{recommendation.get('severity')} - "
                f"{recommendation.get('description')}"
            )

        return "\n".join(lines)

    def _general_context(self):
        lines = []

        layers = self.architecture.get(
            "layers",
            {},
        )

        for layer, modules in layers.items():
            lines.append(
                f"{layer}: "
                f"{', '.join(modules)}"
            )

        return "\n".join(lines)