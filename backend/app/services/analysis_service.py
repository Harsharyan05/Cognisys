from app.parser.repository_scanner import RepositoryScanner
from app.parser.technology_detector import TechnologyDetector
from app.parser.dependency_analyzer import DependencyAnalyzer
from app.parser.architecture_analyzer import ArchitectureAnalyzer

from app.architecture.architecture_engine import ArchitectureEngine


class AnalysisService:

    @staticmethod
    def analyze(repository_path: str):

        scanner = RepositoryScanner()
        detector = TechnologyDetector()
        dependency = DependencyAnalyzer()
        architecture = ArchitectureAnalyzer()
        architecture_engine = ArchitectureEngine(
            repository_path
        )

        repository_result = scanner.scan(
            repository_path
        )

        technology_result = detector.detect(
            repository_path
        )

        dependency_result = dependency.analyze(
            repository_path
        )

        architecture_result = architecture.analyze(
            repository_path
        )

        architecture_intelligence = architecture_engine.analyze()

        return {
            "repository": repository_result,
            "technology": technology_result,
            "dependencies": dependency_result,
            "architecture": {
                "overview": architecture_result,
                "intelligence": architecture_intelligence,
            },
        }
