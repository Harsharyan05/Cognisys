from app.ai.symbol_relationship_index import (
    SymbolRelationshipIndex,
)


def test_get_relationships_returns_all_relationships():
    relationships = [
        {
            "source": "a.py:function:foo",
            "target": "b.py:function:bar",
            "type": "CALLS",
        },
        {
            "source": "b.py:function:bar",
            "target": "a.py:function:foo",
            "type": "CALLED_BY",
        },
    ]

    index = SymbolRelationshipIndex(
        relationships
    )

    result = index.get_relationships(
        "a.py:function:foo"
    )

    assert len(result) == 2


def test_get_callers_returns_calling_symbols():
    relationships = [
        {
            "source": "a.py:function:foo",
            "target": "b.py:function:bar",
            "type": "CALLS",
        },
        {
            "source": "c.py:function:baz",
            "target": "b.py:function:bar",
            "type": "CALLS",
        },
    ]

    index = SymbolRelationshipIndex(
        relationships
    )

    result = index.get_callers(
        "b.py:function:bar"
    )

    assert set(result) == {
        "a.py:function:foo",
        "c.py:function:baz",
    }


def test_get_callees_returns_called_symbols():
    relationships = [
        {
            "source": "a.py:function:foo",
            "target": "b.py:function:bar",
            "type": "CALLS",
        },
        {
            "source": "a.py:function:foo",
            "target": "c.py:function:baz",
            "type": "CALLS",
        },
    ]

    index = SymbolRelationshipIndex(
        relationships
    )

    result = index.get_callees(
        "a.py:function:foo"
    )

    assert set(result) == {
        "b.py:function:bar",
        "c.py:function:baz",
    }


def test_get_importers_returns_importing_modules():
    relationships = [
        {
            "source": "services.py",
            "target": "repositories.py",
            "type": "IMPORTS",
        },
        {
            "source": "controllers.py",
            "target": "repositories.py",
            "type": "IMPORTS",
        },
    ]

    index = SymbolRelationshipIndex(
        relationships
    )

    result = index.get_importers(
        "repositories.py"
    )

    assert set(result) == {
        "services.py",
        "controllers.py",
    }


def test_get_imports_returns_imported_modules():
    relationships = [
        {
            "source": "services.py",
            "target": "repositories.py",
            "type": "IMPORTS",
        },
        {
            "source": "services.py",
            "target": "models.py",
            "type": "IMPORTS",
        },
    ]

    index = SymbolRelationshipIndex(
        relationships
    )

    result = index.get_imports(
        "services.py"
    )

    assert set(result) == {
        "repositories.py",
        "models.py",
    }


def test_get_parent_classes_returns_inherited_classes():
    relationships = [
        {
            "source": "auth.py:class:AdminService",
            "target": "base.py:class:BaseService",
            "type": "INHERITS",
        },
    ]

    index = SymbolRelationshipIndex(
        relationships
    )

    result = index.get_parent_classes(
        "auth.py:class:AdminService"
    )

    assert result == [
        "base.py:class:BaseService"
    ]


def test_get_child_classes_returns_inheriting_classes():
    relationships = [
        {
            "source": "auth.py:class:AdminService",
            "target": "base.py:class:BaseService",
            "type": "INHERITS",
        },
        {
            "source": "user.py:class:UserService",
            "target": "base.py:class:BaseService",
            "type": "INHERITS",
        },
    ]

    index = SymbolRelationshipIndex(
        relationships
    )

    result = index.get_child_classes(
        "base.py:class:BaseService"
    )

    assert set(result) == {
        "auth.py:class:AdminService",
        "user.py:class:UserService",
    }


def test_get_relationships_by_type():
    relationships = [
        {
            "source": "a.py:function:foo",
            "target": "b.py:function:bar",
            "type": "CALLS",
        },
        {
            "source": "a.py",
            "target": "b.py",
            "type": "IMPORTS",
        },
        {
            "source": "c.py:class:Child",
            "target": "c.py:class:Parent",
            "type": "INHERITS",
        },
    ]

    index = SymbolRelationshipIndex(
        relationships
    )

    result = index.get_relationships_by_type(
        "CALLS"
    )

    assert result == [
        {
            "source": "a.py:function:foo",
            "target": "b.py:function:bar",
            "type": "CALLS",
        }
    ]


def test_unknown_symbol_returns_empty_list():
    index = SymbolRelationshipIndex([])

    assert (
        index.get_relationships(
            "unknown:symbol"
        )
        == []
    )

    assert (
        index.get_callers(
            "unknown:symbol"
        )
        == []
    )

    assert (
        index.get_callees(
            "unknown:symbol"
        )
        == []
    )


def test_duplicate_relationships_are_not_returned():
    relationships = [
        {
            "source": "a.py:function:foo",
            "target": "b.py:function:bar",
            "type": "CALLS",
        },
        {
            "source": "a.py:function:foo",
            "target": "b.py:function:bar",
            "type": "CALLS",
        },
    ]

    index = SymbolRelationshipIndex(
        relationships
    )

    result = index.get_relationships(
        "a.py:function:foo"
    )

    assert len(result) == 1