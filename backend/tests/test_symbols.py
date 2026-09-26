from pathlib import Path

from app.parser.symbol_extractor import SymbolExtractor


def test_symbol_extractor_finds_classes_and_functions(tmp_path):
    repository = tmp_path / "repo"
    repository.mkdir()

    source_file = repository / "example.py"

    source_file.write_text(
        """
class UserService:

    def create_user(self):
        pass


def helper_function():
    pass
""",
        encoding="utf-8",
    )

    extractor = SymbolExtractor()

    result = extractor.extract(str(repository))

    assert "example.py" in result

    symbols = result["example.py"]

    assert len(symbols["classes"]) == 1
    assert symbols["classes"][0]["name"] == "UserService"

    assert len(symbols["functions"]) == 2

    function_names = {
        function["name"]
        for function in symbols["functions"]
    }

    assert "create_user" in function_names
    assert "helper_function" in function_names


def test_symbol_extractor_records_line_numbers(tmp_path):
    repository = tmp_path / "repo"
    repository.mkdir()

    source_file = repository / "example.py"

    source_file.write_text(
        """class UserService:

    def create_user(self):
        pass
""",
        encoding="utf-8",
    )

    extractor = SymbolExtractor()

    result = extractor.extract(str(repository))

    symbols = result["example.py"]

    assert symbols["classes"][0]["name"] == "UserService"
    assert symbols["classes"][0]["line"] == 1

    create_user = next(
        function
        for function in symbols["functions"]
        if function["name"] == "create_user"
    )

    assert create_user["line"] == 3
    
def test_symbol_extractor_extracts_symbol_source_code(tmp_path):
    repository = tmp_path / "repo"
    repository.mkdir()

    source_file = repository / "example.py"

    source_file.write_text(
        """class UserService:

    def create_user(self):
        return "created"


def helper_function():
    return "helper"
""",
        encoding="utf-8",
    )

    extractor = SymbolExtractor()

    result = extractor.extract(str(repository))

    symbols = result["example.py"]

    user_service = symbols["classes"][0]

    assert user_service["name"] == "UserService"
    assert "class UserService:" in user_service["code"]
    assert "def create_user(self):" in user_service["code"]
    assert 'return "created"' in user_service["code"]

    helper = next(
        function
        for function in symbols["functions"]
        if function["name"] == "helper_function"
    )

    assert "def helper_function():" in helper["code"]
    assert 'return "helper"' in helper["code"] 
    
def test_symbol_extractor_tracks_parent_class_for_methods(tmp_path):
    repository = tmp_path / "repo"
    repository.mkdir()

    source_file = repository / "example.py"

    source_file.write_text(
        """class UserService:

    def create_user(self):
        return "created"

    async def delete_user(self):
        return "deleted"


def helper_function():
    return "helper"
""",
        encoding="utf-8",
    )

    extractor = SymbolExtractor()

    result = extractor.extract(str(repository))

    symbols = result["example.py"]

    create_user = next(
        function
        for function in symbols["functions"]
        if function["name"] == "create_user"
    )

    delete_user = next(
        function
        for function in symbols["functions"]
        if function["name"] == "delete_user"
    )

    helper = next(
        function
        for function in symbols["functions"]
        if function["name"] == "helper_function"
    )

    assert create_user["parent_class"] == "UserService"
    assert delete_user["parent_class"] == "UserService"

    assert helper["parent_class"] is None    

def test_symbol_extractor_assigns_symbol_types(tmp_path):
    repository = tmp_path / "repo"
    repository.mkdir()

    source_file = repository / "example.py"

    source_file.write_text(
        """class UserService:

    def create_user(self):
        return "created"


def helper_function():
    return "helper"
""",
        encoding="utf-8",
    )

    extractor = SymbolExtractor()

    result = extractor.extract(str(repository))

    symbols = result["example.py"]

    user_service = symbols["classes"][0]

    create_user = next(
        function
        for function in symbols["functions"]
        if function["name"] == "create_user"
    )

    helper = next(
        function
        for function in symbols["functions"]
        if function["name"] == "helper_function"
    )

    assert user_service["type"] == "class"
    assert create_user["type"] == "method"
    assert helper["type"] == "function"    

def test_symbol_extractor_generates_stable_symbol_ids(tmp_path):
    repository = tmp_path / "repo"
    repository.mkdir()

    source_file = repository / "example.py"

    source_file.write_text(
        """class UserService:

    def create_user(self):
        return "created"


def helper_function():
    return "helper"
""",
        encoding="utf-8",
    )

    extractor = SymbolExtractor()

    result = extractor.extract(str(repository))

    symbols = result["example.py"]

    user_service = symbols["classes"][0]

    create_user = next(
        function
        for function in symbols["functions"]
        if function["name"] == "create_user"
    )

    helper = next(
        function
        for function in symbols["functions"]
        if function["name"] == "helper_function"
    )

    assert user_service["id"] == "example.py:class:UserService"

    assert (
        create_user["id"]
        == "example.py:method:UserService.create_user"
    )

    assert helper["id"] == "example.py:function:helper_function"    