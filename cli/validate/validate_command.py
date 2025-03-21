import logging
import pathlib
from typing import List

from cli.const.constant import FileTypes
from cli.utils.file_helper import get_root_dir
from cli.validate.validate_plugin import ValidatePlugin

logger = logging.getLogger(__name__)


class ValidateCommand:
    def fill_names_by_folder(self, path: str) -> str:
        files = (p.resolve() for p in pathlib.Path(path).glob("**/*") if p.suffix in {FileTypes.YML, FileTypes.SQL})
        all_filenames: List[str] = []
        for config_file in files:
            all_filenames.append((str(config_file)).replace(get_root_dir() + "/", ""))
        return ",".join(all_filenames)

    def fill_names_if_empty(self, filenames: str) -> str:
        if not filenames:
            models_macros = self.fill_names_by_folder(get_root_dir() + "/macros")
            models_filenames = self.fill_names_by_folder(get_root_dir() + "/models")
            return ",".join([models_macros, models_filenames])
        return filenames

    def validate_files(self, filenames: str, validators: List[ValidatePlugin]) -> bool:
        filenames = self.fill_names_if_empty(filenames)
        filenames_list = filenames.split(",")
        for filename in filenames_list:
            filename = filename.strip()
            for validator in validators:
                if validator.is_applicable(filename):
                    logger.debug(validator.add_plugin_name_to_message(f"Validating {filename}"))
                    data = validator.load_file(filename)
                    if data and not validator.validate(filename, data):
                        return False
                else:
                    logger.debug(validator.add_plugin_name_to_message(f"{filename} not applicable"))
        return True
