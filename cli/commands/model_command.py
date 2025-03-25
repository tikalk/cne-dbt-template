import logging
import os
import shutil
from abc import ABC
from typing import Optional

from cookiecutter.exceptions import OutputDirExistsException
from cookiecutter.main import cookiecutter
from rich.prompt import Prompt

from cli.config import ini_config
from cli.const.const_model import ModelCode, ModelType
from cli.const.constant import Logs
from cli.utils.file_helper import get_folder_names, get_models_dir, get_resources_dir
from cli.utils.prompt_utils import PromptUtils
from cli.utils.user_options import UserOptions

logger = logging.getLogger(__name__)


class ModelCommands(ABC):

    def assign_code(self, code_type: str) -> ModelCode:
        if not code_type:
            logger.info("Model code type not given. Loading available types...")
            types = UserOptions(ModelCode.get_valid_types(), sort_options=False)
            selected_type = types.select("Please choose type number / name to use", default_selection=ModelCode.SQL.value)
            return ModelCode.from_str(selected_type)
        return ModelCode.from_str(code_type)

    def assign_tool(self, tool_name) -> str:
        if not tool_name:
            logger.info("Tool type not given. Loading available tools...")
            tool_names = get_folder_names(os.path.join(get_models_dir(), "tools"))
            types = UserOptions(tool_names, sort_options=False)
            selected_type = types.select("Please choose type number / name to use", default_selection=ModelType.GOLD.to_str())
            return selected_type
        return tool_name

    def assign_type(self, type: str) -> ModelType:
        if not type:
            logger.info("Model type not given. Loading available types...")
            types = UserOptions(ModelType.get_valid_types(), sort_options=False)
            selected_type = types.select("Please choose type number / name to use", default_selection=ModelType.GOLD.to_str())
            return ModelType.from_str(selected_type)
        return ModelType.from_str(type)

    def get_model_type_by_dir(self, file_name_path: str) -> ModelType:
        source_base_folder = ini_config.get("model", "SOURCE_FOLDER", fallback="silver/base")
        staging_base_folder = ini_config.get("model", "STAGING_BASE_FOLDER", fallback="silver/base")
        staging_compatible_folder = ini_config.get("model", "STAGING_COMPATIBLE_FOLDER", fallback="silver/staging")
        gold_folder = ini_config.get("model", "MARTS_FOLDER", fallback="gold")

        if source_base_folder in file_name_path:
            return ModelType.SOURCE
        if staging_base_folder in file_name_path:
            return ModelType.BASE
        if staging_compatible_folder in file_name_path:
            return ModelType.STAGING
        if gold_folder in file_name_path:
            return ModelType.GOLD
        raise ValueError(f"Unknown model type for file name path: {file_name_path}")

    def get_access_by_type(self, model_type: ModelType):
        match model_type:
            case ModelType.SOURCE:
                return "private"
            case ModelType.BASE:
                return "private"
            case ModelType.STAGING:
                return "protected"
            case ModelType.GOLD:
                return "public"

    def get_model_dir_by_type(self, domain: str, model_type: ModelType, name: str, tool_name: Optional[str] = None) -> str:
        file_name, _ = self.get_model_file_name(domain, model_type, ModelCode.SQL, name, tool_name)
        file_name, _ = os.path.splitext(file_name)
        file_name = file_name.replace("___", "__")
        return f"{ModelType.get_model_base_dir_by_type(domain, model_type,tool_name)}/{file_name}"

    def get_model_prefix(self, model_type: ModelType) -> str:
        return f"{ModelType.get_model_prefix(ModelType.STAGING)}__" if model_type == ModelType.STAGING or model_type == ModelType.BASE else "__"

    def get_file_prefix(self, domain: str, model_type: ModelType, tool_name: Optional[str] = None):
        domain_name = tool_name if tool_name else domain
        file_prefix = f"{domain_name}_{self.get_model_prefix(model_type)}".replace("___", "__")
        return file_prefix

    def get_model_file_name(self, domain: str, model_type: ModelType, model_code: ModelCode, name: str, tool_name: Optional[str] = None):
        name_prefix = self.get_model_prefix(model_type)
        domain_name = tool_name if tool_name else domain
        domain_name = domain_name.split("/")[-1]
        expected_model_name = f"{domain_name}_{name_prefix}{name}.{model_code.to_extension()}"
        expected_model_name = expected_model_name.replace("___", "__")
        expected_model_metadata_name = f"{domain_name}_{name_prefix}{name}.yml"
        return expected_model_name, expected_model_metadata_name

    def is_model_name_valid(
        self, domain: str, model_type: ModelType, candidate_name: str, tool_name: Optional[str] = None
    ) -> tuple[bool, Optional[str]]:
        if not candidate_name:
            logger.error(f"{type} model must have a name.")
            return False, None
        candidate_name = candidate_name.lower()
        model_dir = self.get_model_dir_by_type(domain, model_type, candidate_name, tool_name)
        expected_model_name, expected_model_metadata_name = self.get_model_file_name(domain, model_type, ModelCode.SQL, candidate_name)
        if os.path.isfile(f"{model_dir}/{expected_model_name}") or os.path.isfile(f"{model_dir}/{expected_model_metadata_name}"):
            logger.error(f"{type} model with name {candidate_name} already exists with its metadata.")
            return False, None
        return True, candidate_name

    def assign_name(self, domain: str, model_type: ModelType, name: str, tool_name: Optional[str] = None) -> str:
        if not name:
            logger.info("Name was not given. Please enter model name...")
            name = Prompt.ask(PromptUtils.allow_abort("Please give a name for the new model"))
            UserOptions.check_if_abort_requested(name)
            name_is_valid, validated_name = self.is_model_name_valid(domain, model_type, name, tool_name)
            while not name_is_valid:
                name = Prompt.ask(PromptUtils.allow_abort("Please choose another name for the new model"))
                UserOptions.check_if_abort_requested(name)
                name_is_valid, validated_name = self.is_model_name_valid(domain, model_type, name)
            return validated_name if validated_name is not None else name
        return name

    def create_model(self, domain: str, model_type: ModelType, model_code: ModelCode, name: str, tool_name: Optional[str] = None) -> None:
        """Creates a new model in the specified domain with the given type and name."""
        domain_only = os.path.basename(os.path.normpath(domain))
        model_dir = self.get_model_dir_by_type(domain, model_type, name, tool_name)
        match model_code:
            case ModelCode.SQL:
                file_suffix = ".sql"
            case ModelCode.PYTHON:
                file_suffix = ".py"
        match model_type:
            case ModelType.BASE:
                model_template = os.path.join(get_resources_dir(), "templates", "models", f"base_model_template{file_suffix}")
            case ModelType.STAGING:
                model_template = os.path.join(get_resources_dir(), "templates", "models", f"staging_model_template{file_suffix}")
            case ModelType.GOLD:
                model_template = os.path.join(get_resources_dir(), "templates", "models", f"gold_model_template{file_suffix}")

        model_file_name, _ = self.get_model_file_name(domain_only, model_type, model_code, name, tool_name)
        filename_without_ext = os.path.splitext(os.path.basename(model_file_name))[0]
        model_prefix = self.get_model_prefix(model_type)
        if model_prefix == "__":
            model_prefix = "_"
        if tool_name:
            extra_context = {
                "model_name": name,
                "full_model_name": filename_without_ext,
                "domain_name": tool_name,
                "prefix": model_prefix,
            }
        else:
            extra_context = {
                "model_name": name,
                "full_model_name": filename_without_ext,
                "domain_name": domain_only,
                "prefix": model_prefix,
            }

        try:
            cookiecutter(
                template=os.path.join(get_resources_dir(), "templates", "models", "model"),
                no_input=True,
                extra_context=extra_context,
                output_dir=ModelType.get_model_base_dir_by_type(domain, model_type, tool_name),
                overwrite_if_exists=False,
                skip_if_file_exists=False,
            )

            shutil.copyfile(model_template, f"{model_dir}/{model_file_name}")

            colored_model = PromptUtils.color_text(name, Logs.MODEL_HIGHLIGHT)
            logger.info(f"Model {colored_model} successfully created in {domain_only}/{model_type}. :white_check_mark:")
            relative_path = model_dir.replace(get_models_dir(), "")
            logger.info(f"Model file can be found at {relative_path}/{model_file_name}")
            logger.info(f"Model metadata file can be found at {relative_path}/{model_file_name.replace('.sql', '.yml').replace('.py', '.yml')}")
        except OutputDirExistsException:
            logger.error("Model already exists by that name. Please choose another name.")
