import logging

from cli.validate.validate_yaml_plugin import ValidateYmlModelPlugin

logger = logging.getLogger(__name__)


class ModelValidatePlugin(ValidateYmlModelPlugin):
    def is_applicable(self, file_name: str) -> bool:
        return super().is_applicable_models_only(file_name)

    def validate_model_name(self, model) -> bool:
        return True
