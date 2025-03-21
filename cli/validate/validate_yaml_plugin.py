import logging

from cli.const.constant import FileTypes
from cli.validate.validate_plugin import ValidatePlugin

logger = logging.getLogger(__name__)


class ValidateYmlPlugin(ValidatePlugin):
    def is_applicable(self, file_name: str) -> bool:
        return super().is_applicable(file_name) and file_name.endswith(FileTypes.YML)


class ValidateYmlModelPlugin(ValidateYmlPlugin):
    def is_applicable_models_only(self, file_name: str) -> bool:
        return super().is_applicable(file_name) and "/exposures/" not in file_name and "/source/" not in file_name

    def is_applicable(self, file_name: str) -> bool:
        return super().is_applicable(file_name) and "models/" in file_name and file_name.endswith(FileTypes.YML)
