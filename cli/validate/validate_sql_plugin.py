from cli.const.constant import FileTypes
from cli.validate.validate_plugin import ValidatePlugin


class ValidateSqlPlugin(ValidatePlugin):
    def is_applicable(self, file_name: str) -> bool:
        return super().is_applicable(file_name) and file_name.endswith(FileTypes.SQL)

    def load_file(self, file_name: str) -> object:
        return file_name
