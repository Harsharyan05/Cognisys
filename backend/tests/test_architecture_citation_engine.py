from app.ai.architecture_citation_engine import (
    ArchitectureCitationEngine,
)


def sample_analysis():
    return {
        "layers": {
            "Business": [
                "app/services",
            ],
            "Presentation": [
                "app/api",
            ],
        },
        "dependency_graph": {
            "app.api.auth": [
                "app.services.auth_service",
            ],
            "app.services.auth_service": [
                "app.database.user_repository",
            ],
        },
        "cycles": [
            [
                "app.a",
                "app.b",
                "app.a",
            ],
        ],
        "hotspots": [
            {
                "module": "app.services.auth_service",
                "fan_in": 5,
                "fan_out": 2,
                "score": 12,
                "risk": "HIGH",
            }
        ],
        "patterns": [
            {
                "pattern": "Layered Architecture",
                "confidence": 0.95,
            }
        ],
        "recommendations": [
            {
                "message": "Review high-risk hotspot.",
                "severity": "HIGH",
            }
        ],
    }


def test_generates_layer_citations():
    engine = ArchitectureCitationEngine(
        sample_analysis()
    )

    citations = engine.generate()

    assert any(
        citation["type"] == "architecture_layer"
        for citation in citations
    )


def test_generates_dependency_citations():
    engine = ArchitectureCitationEngine(
        sample_analysis()
    )

    citations = engine.generate()

    assert any(
        citation["type"] == "architecture_dependency"
        for citation in citations
    )


def test_generates_cycle_citations():
    engine = ArchitectureCitationEngine(
        sample_analysis()
    )

    citations = engine.generate()

    assert any(
        citation["type"] == "architecture_cycle"
        for citation in citations
    )


def test_generates_hotspot_citations():
    engine = ArchitectureCitationEngine(
        sample_analysis()
    )

    citations = engine.generate()

    assert any(
        citation["type"] == "architecture_hotspot"
        for citation in citations
    )


def test_generates_pattern_citations():
    engine = ArchitectureCitationEngine(
        sample_analysis()
    )

    citations = engine.generate()

    assert any(
        citation["type"] == "architecture_pattern"
        for citation in citations
    )


def test_generates_recommendation_citations():
    engine = ArchitectureCitationEngine(
        sample_analysis()
    )

    citations = engine.generate()

    assert any(
        citation["type"] == "architecture_recommendation"
        for citation in citations
    )


def test_each_citation_has_id():
    engine = ArchitectureCitationEngine(
        sample_analysis()
    )

    citations = engine.generate()

    assert citations

    for citation in citations:
        assert "id" in citation
        assert citation["id"].startswith("ARCH-")


def test_each_citation_has_source():
    engine = ArchitectureCitationEngine(
        sample_analysis()
    )

    citations = engine.generate()

    assert citations

    for citation in citations:
        assert "source" in citation