import logging
import os
from pathlib import Path
from typing import Optional

from cli.const.const_model import ModelType
from cli.const.constant import FileTypes
from cli.utils.file_helper import get_models_dir
from cli.validate.validate_plugin import ValidatePlugin

logger = logging.getLogger(__name__)


class MacroNameValidatePlugin(ValidatePlugin):
    def is_applicable(self, file_name: str) -> bool:
        return (
            super().is_applicable(file_name)
            and (file_name.startswith("macro"))
            and (file_name.endswith(FileTypes.SQL) or file_name.endswith(FileTypes.YML))
        )

    def load_file(self, file_name: str) -> object:
        return file_name

    def validate(self, file_path_name: str, data: object) -> bool:
        try:
            parent_dir = str(Path(file_path_name).parent).split("/")[-1]
            file_name = Path(file_path_name).stem
            if parent_dir != file_name:
                logger.error(self.add_plugin_name_to_message(f"macro {file_name} must be in folder {file_name}"))
                return False

            file_name, extension = os.path.splitext(file_path_name)  # Splits the name and extension
            # check if file exists

            if extension == FileTypes.SQL and not os.path.exists(file_path_name.replace(FileTypes.SQL, FileTypes.YML)):
                logger.error(self.add_plugin_name_to_message(f"macro {file_name} must have both yml and sql"))
                return False

            if extension == FileTypes.YML and not os.path.exists(file_path_name.replace(FileTypes.YML, FileTypes.SQL)):
                logger.error(self.add_plugin_name_to_message(f"macro {file_name} must have both yml and sql"))
                return False

            return True
        except Exception as e:
            logger.error("ModelNameValidatePlugin ", e)
            return False

    def _get_model_label(self, domain: str, file_name: str, tool_name: Optional[str] = None) -> ModelType:
        base_dir = ModelType.get_model_base_dir_by_type(domain, ModelType.BASE, tool_name).replace(get_models_dir(), "models")
        staging_dir = ModelType.get_model_base_dir_by_type(domain, ModelType.STAGING, tool_name).replace(get_models_dir(), "models")
        gold_dir = ModelType.get_model_base_dir_by_type(domain, ModelType.GOLD, tool_name).replace(get_models_dir(), "models")
        exposure_dir = ModelType.get_model_base_dir_by_type(domain, ModelType.EXPOSURES, tool_name).replace(get_models_dir(), "models")
        if file_name.startswith(base_dir):
            return ModelType.BASE
        if file_name.startswith(staging_dir):
            return ModelType.STAGING
        if file_name.startswith(gold_dir):
            return ModelType.GOLD
        if file_name.startswith(exposure_dir):
            return ModelType.EXPOSURES
        return None
