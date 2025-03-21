from cli.const.const_model import ModelCode, ModelType


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


def test_model_type_get_valid_types():
    assert ModelType.get_valid_types() == [
        "Model - Silver Base",
        "Model - Silver Staging",
        "Model - Gold",
    ]


def test_model_type_from_str():
    assert ModelType.from_str("source") == ModelType.SOURCE
    assert ModelType.from_str("Model - Source") == ModelType.SOURCE
    assert ModelType.from_str("base") == ModelType.BASE
    assert ModelType.from_str("Model - Silver Base") == ModelType.BASE
    assert ModelType.from_str("staging") == ModelType.STAGING
    assert ModelType.from_str("Model - Silver Staging") == ModelType.STAGING
    assert ModelType.from_str("gold") == ModelType.GOLD
    assert ModelType.from_str("Model - Gold") == ModelType.GOLD
    assert ModelType.from_str("exposures") == ModelType.EXPOSURES
    assert ModelType.from_str("Model - Exposure") == ModelType.EXPOSURES
    assert ModelType.from_str("unknown") is None
