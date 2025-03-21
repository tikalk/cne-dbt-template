import logging
import os
from typing import Optional

from cli.commands.model_command import ModelCommands
from cli.const.const_model import ModelType
from cli.const.constant import FileTypes
from cli.utils.file_helper import get_models_dir
from cli.validate.validate_plugin import ValidatePlugin

logger = logging.getLogger(__name__)


class ModelNameValidatePlugin(ValidatePlugin):
    def is_applicable(self, file_name: str) -> bool:
        return (
            super().is_applicable(file_name)
            and (file_name.startswith("models"))
            and (file_name.endswith(FileTypes.SQL) or file_name.endswith(FileTypes.YML))
        )

    def load_file(self, file_name: str) -> object:
        return file_name

    def validate(self, file_path_name: str, data: object) -> bool:
        try:
            file_name = os.path.basename(file_path_name)
            domain = file_path_name.split("/")[1].strip()
            sub_domain: Optional[str] = file_path_name.split("/")[2].strip()
            if ModelType.from_str(sub_domain):
                sub_domain = None
            if file_name == f"{domain}_props.yml" or file_name == f"{sub_domain}_props.yml":
                return True

            check_domain = domain
            if sub_domain:
                check_domain = check_domain + "/" + sub_domain
            model_type = self._get_model_label(check_domain, file_path_name, None)
            if model_type is None:
                logger.error(self.add_plugin_name_to_message(f"model {file_path_name} is not in staging or marts directory"))
                return False
            check_domain = domain if not sub_domain else sub_domain
            file_prefix = ModelCommands().get_file_prefix(check_domain, model_type, None)
            if not file_name.startswith(file_prefix):
                logger.error(self.add_plugin_name_to_message(f"model {file_name} must start with prefix {file_prefix}"))
                return False

            file_name_suffix = file_name.replace(file_prefix, "")
            if not file_name_suffix[0].isalnum():
                logger.error(self.add_plugin_name_to_message(f"model {file_name} must start with letter"))
                return False

            # d = DomainResourceLocation(domain)
            # file_prefix = d.get_model_filename_prefix(model_type)
            # model_name = os.path.basename(file_name)
            # if not model_name.startswith(file_prefix):
            #     logger.error(self.add_plugin_name_to_message(f"Model {file_name} name is not according to convention [domain_type__]."))
            #     return False
            # if model_name.count("__") != 1:
            #     logger.error(
            #         self.add_plugin_name_to_message(f"Model {file_name} name is not according to convention [domain_type__]. __ can be only once")
            #     )
            #     return False
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
