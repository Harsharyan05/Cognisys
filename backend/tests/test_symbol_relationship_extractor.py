import textwrap

from app.parser.symbol_relationship_extractor import (
    SymbolRelationshipExtractor,
)


def create_repository(tmp_path, files):
    for relative_path, content in files.items():
        file_path = tmp_path / relative_path
        file_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )
        file_path.write_text(
            textwrap.dedent(content),
            encoding="utf-8",
        )

    return tmp_path


def test_extracts_function_call_relationship(tmp_path):
    repository = create_repository(
        tmp_path,
        {
            "services.py": """
                def authenticate():
                    validate_token()

                def validate_token():
                    pass
            """
        },
    )

    extractor = SymbolRelationshipExtractor(
        repository
    )

    relationships = extractor.extract()

    assert {
        "source": "services.py:function:authenticate",
        "target": "services.py:function:validate_token",
        "type": "CALLS",
    } in relationships


def test_extracts_reverse_called_by_relationship(tmp_path):
    repository = create_repository(
        tmp_path,
        {
            "services.py": """
                def authenticate():
                    validate_token()

                def validate_token():
                    pass
            """
        },
    )

    extractor = SymbolRelationshipExtractor(
        repository
    )

    relationships = extractor.extract()

    assert {
        "source": "services.py:function:validate_token",
        "target": "services.py:function:authenticate",
        "type": "CALLED_BY",
    } in relationships


def test_extracts_import_relationship(tmp_path):
    repository = create_repository(
        tmp_path,
        {
            "services.py": """
                from repositories import UserRepository

                def authenticate():
                    repository = UserRepository()
            """,
            "repositories.py": """
                class UserRepository:
                    pass
            """,
        },
    )

    extractor = SymbolRelationshipExtractor(
        repository
    )

    relationships = extractor.extract()

    assert {
        "source": "services.py",
        "target": "repositories.py",
        "type": "IMPORTS",
    } in relationships


def test_extracts_reverse_imported_by_relationship(tmp_path):
    repository = create_repository(
        tmp_path,
        {
            "services.py": """
                from repositories import UserRepository

                def authenticate():
                    repository = UserRepository()
            """,
            "repositories.py": """
                class UserRepository:
                    pass
            """,
        },
    )

    extractor = SymbolRelationshipExtractor(
        repository
    )

    relationships = extractor.extract()

    assert {
        "source": "repositories.py",
        "target": "services.py",
        "type": "IMPORTED_BY",
    } in relationships


def test_extracts_inheritance_relationship(tmp_path):
    repository = create_repository(
        tmp_path,
        {
            "models.py": """
                class User:
                    pass

                class Admin(User):
                    pass
            """
        },
    )

    extractor = SymbolRelationshipExtractor(
        repository
    )

    relationships = extractor.extract()

    assert {
        "source": "models.py:class:Admin",
        "target": "models.py:class:User",
        "type": "INHERITS",
    } in relationships


def test_extracts_reverse_inherited_by_relationship(tmp_path):
    repository = create_repository(
        tmp_path,
        {
            "models.py": """
                class User:
                    pass

                class Admin(User):
                    pass
            """
        },
    )

    extractor = SymbolRelationshipExtractor(
        repository
    )

    relationships = extractor.extract()

    assert {
        "source": "models.py:class:User",
        "target": "models.py:class:Admin",
        "type": "INHERITED_BY",
    } in relationships


def test_does_not_create_duplicate_relationships(tmp_path):
    repository = create_repository(
        tmp_path,
        {
            "services.py": """
                def authenticate():
                    validate_token()
                    validate_token()

                def validate_token():
                    pass
            """
        },
    )

    extractor = SymbolRelationshipExtractor(
        repository
    )

    relationships = extractor.extract()

    matching = [
        relationship
        for relationship in relationships
        if relationship["type"] == "CALLS"
        and relationship["source"]
        == "services.py:function:authenticate"
        and relationship["target"]
        == "services.py:function:validate_token"
    ]

    assert len(matching) == 1


def test_handles_unknown_called_symbol(tmp_path):
    repository = create_repository(
        tmp_path,
        {
            "services.py": """
                def authenticate():
                    external_function()
            """
        },
    )

    extractor = SymbolRelationshipExtractor(
        repository
    )

    relationships = extractor.extract()

    calls = [
        relationship
        for relationship in relationships
        if relationship["type"] == "CALLS"
    ]

    assert calls == []


def test_skips_invalid_python_files(tmp_path):
    repository = create_repository(
        tmp_path,
        {
            "valid.py": """
                def authenticate():
                    pass
            """,
            "invalid.py": """
                def broken(
            """,
        },
    )

    extractor = SymbolRelationshipExtractor(
        repository
    )

    relationships = extractor.extract()

    assert isinstance(relationships, list)