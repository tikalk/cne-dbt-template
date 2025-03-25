from cli.const.const_model import ModelCode


def test_model_code_get_valid_types():
    assert ModelCode.get_valid_types() == ["Model - Sql", "Model - Python"]


def test_model_code_from_str():
    assert ModelCode.from_str("sql") == ModelCode.SQL
    assert ModelCode.from_str("Model - Sql") == ModelCode.SQL
    assert ModelCode.from_str("python") == ModelCode.PYTHON
    assert ModelCode.from_str("Model - Python") == ModelCode.PYTHON
    assert ModelCode.from_str("unknown") is None


def test_model_code_to_extension():
    assert ModelCode.SQL.to_extension() == "sql"
    assert ModelCode.PYTHON.to_extension() == "py"
