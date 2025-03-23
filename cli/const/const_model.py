from typing import Optional

from cli.config import ini_config
from cli.const.const_base import SuperEnum
from cli.utils.file_helper import get_models_dir


class ModelCode(SuperEnum):
    SQL = "Model - Sql"
    PYTHON = "Model - Python"

    @staticmethod
    def get_valid_types():
        return [
            ModelCode.SQL.value,
            ModelCode.PYTHON.value,
        ]

    @staticmethod
    def from_str(label):
        lower_label = label.lower()
        if lower_label in [ModelCode.SQL.name.lower(), ModelCode.SQL.value.lower()]:
            return ModelCode.SQL
        elif lower_label in [ModelCode.PYTHON.name.lower(), ModelCode.PYTHON.value.lower()]:
            return ModelCode.PYTHON

    def to_extension(self):
        match self:
            case ModelCode.SQL:
                return "sql"
            case ModelCode.PYTHON:
                return "py"


class ModelType(SuperEnum):
    SOURCE = "Model - Source"
    BASE = "Model - Silver Base"
    STAGING = "Model - Silver Staging"
    GOLD = "Model - Gold"
    EXPOSURES = "Model - Exposure"

    def get_layer_name(self):
        match self:
            case ModelType.SOURCE:
                return ini_config.get("model", "SOURCE_LAYER", fallback="source")
            case ModelType.BASE:
                return ini_config.get("model", "BASE_LAYER", fallback="staging")
            case ModelType.STAGING:
                return ini_config.get("model", "STAGING_LAYER", fallback="staging")
            case ModelType.GOLD:
                return ini_config.get("model", "MARTS_LAYER", fallback="marts")
            case _:
                raise ValueError(f"Unknown model type: {self.name}")

    def get_title_name(self):
        match self:
            case ModelType.SOURCE:
                return ini_config.get("model", "SOURCE_TITLE", fallback=self.value)
            case ModelType.BASE:
                return ini_config.get("model", "BASE_TITLE", fallback=self.value)
            case ModelType.STAGING:
                return ini_config.get("model", "STAGING_TITLE", fallback=self.value)
            case ModelType.GOLD:
                return ini_config.get("model", "MARTS_TITLE", fallback=self.value)
            case _:
                raise ValueError(f"Unknown model type: {self.name}")

    def to_str(self) -> str:
        get_title_name = self.get_title_name()
        return f"Model - {get_title_name}"

    @staticmethod
    def get_valid_types():
        return [model_type.to_str() for model_type in ModelType.get_model_valid_types()]

    @staticmethod
    def get_model_valid_types():
        return [
            ModelType.BASE,
            ModelType.STAGING,
            ModelType.GOLD,
        ]

    @staticmethod
    def from_str(label: str) -> Optional["ModelType"]:
        lower_label = label.lower()
        source_custom_name = ini_config.get("model", "SOURCE_LAYER", fallback="source")
        base_custom_name = ini_config.get("model", "BASE_LAYER", fallback="source")
        staging_custom_name = ini_config.get("model", "STAGING_LAYER", fallback="source")
        gold_custom_name = ini_config.get("model", "MARTS_LAYER", fallback="source")

        if lower_label in [source_custom_name, ModelType.SOURCE.name.lower(), ModelType.SOURCE.value.lower(), ModelType.SOURCE.to_str().lower()]:  # type: ignore
            return ModelType.SOURCE  # type: ignore
        elif lower_label in [base_custom_name, ModelType.BASE.name.lower(), ModelType.BASE.value.lower(), ModelType.BASE.to_str().lower()]:  # type: ignore
            return ModelType.BASE  # type: ignore
        elif lower_label in [staging_custom_name, ModelType.STAGING.name.lower(), ModelType.STAGING.value.lower(), ModelType.STAGING.to_str().lower()]:  # type: ignore
            return ModelType.STAGING  # type: ignore
        elif lower_label in [gold_custom_name, ModelType.GOLD.name.lower(), ModelType.GOLD.value.lower(), ModelType.GOLD.to_str().lower()]:  # type: ignore
            return ModelType.GOLD  # type: ignore
        else:
            return None

    @staticmethod
    def get_model_prefix(model_type: "ModelType") -> str:
        match model_type:
            case ModelType.SOURCE:
                return ini_config.get("model", "SOURCE_PREFIX", fallback="slv")
            case ModelType.BASE:
                return ini_config.get("model", "BASE_PREFIX", fallback="slv")
            case ModelType.STAGING:
                return ini_config.get("model", "STAGING_PREFIX", fallback="slv")
            case ModelType.GOLD:
                return ini_config.get("model", "MARTS_PREFIX", fallback="slv")
            case _:
                raise ValueError(f"Unknown model type: {model_type}")

    @staticmethod
    def get_model_base_dir_by_type(domain: str, type: "ModelType", tool_name: Optional[str] = None) -> str:
        staging_base_folder = ini_config.get("model", "STAGING_BASE_FOLDER", fallback="silver/base")
        staging_compatible_folder = ini_config.get("model", "STAGING_COMPATIBLE_FOLDER", fallback="silver/staging")
        gold_folder = ini_config.get("model", "MARTS_FOLDER", fallback="gold")
        if not tool_name:
            tool_name = ""
        else:
            tool_name = f"/{tool_name}"
        if type == ModelType.SOURCE:
            return f"{get_models_dir()}{domain}/source"
        elif type == ModelType.BASE:
            return f"{get_models_dir()}/{domain}{tool_name}/{staging_base_folder}"
        elif type == ModelType.STAGING:
            return f"{get_models_dir()}/{domain}{tool_name}/{staging_compatible_folder}"
        elif type == ModelType.GOLD:
            return f"{get_models_dir()}/{domain}{tool_name}/{gold_folder}"
        elif type == ModelType.EXPOSURES:
            return f"{get_models_dir()}/{domain}/exposures"
        else:
            return ""
