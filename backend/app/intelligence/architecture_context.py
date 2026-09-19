class ArchitectureContext:
    """
    Provides a structured view of repository architecture
    for the intelligence layer.
    """

    def __init__(self, analysis: dict):
        self.analysis = analysis

    def get_layers(self):
        return self.analysis.get("layers", {})

    def get_dependency_graph(self):
        return self.analysis.get("dependency_graph", {})

    def get_cycles(self):
        return self.analysis.get("cycles", [])

    def get_hotspots(self):
        return self.analysis.get("hotspots", [])

    def get_patterns(self):
        return self.analysis.get("patterns", [])

    def get_recommendations(self):
        return self.analysis.get("recommendations", [])