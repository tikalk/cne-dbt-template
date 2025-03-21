import logging
import os
from abc import ABC
from typing import Optional

from cookiecutter.exceptions import OutputDirExistsException
from cookiecutter.main import cookiecutter
from rich.prompt import Prompt

from cli.const.constant import Logs
from cli.utils.file_helper import (
    get_folder_content,
    get_macros_dir,
    get_resources_dir,
)
from cli.utils.prompt_utils import PromptUtils
from cli.utils.user_options import UserOptions

logger = logging.getLogger(__name__)


class MacroCommands(ABC):
    internal_macros = ["create_database", "delete_database", "generate_schema_name", "get_custom_alias"]

    def is_macro_dir(self, folder_path: str) -> bool:
        folder_name = os.path.basename(folder_path)
        sql_file = f"{folder_name}.sql"
        yml_file = f"{folder_name}.yml"
        files_in_folder = set(os.listdir(folder_path))
        if sql_file in files_in_folder and yml_file in files_in_folder:
            return True
        else:
            return False

    def query_for_nested_folder(self, path: str) -> Optional[str]:
        paths = get_folder_content(path)
        filtered_list = [item for item in paths if item not in self.internal_macros]
        if self.is_macro_dir(path):
            return None

        filtered_list.insert(0, "Current Dir")
        types = UserOptions(filtered_list, sort_options=False)
        selected_type = types.select("Please choose type number / name to use")
        if selected_type != "Current Dir":
            sub_folder = self.query_for_nested_folder(os.path.join(path, selected_type))
            if not sub_folder:
                return path
            else:
                return sub_folder
        return path

    def assign_path(self, path: str) -> Optional[str]:
        if not path:
            logger.info("Path not given. Loading available paths...")
            return self.query_for_nested_folder(get_macros_dir())
        return path

    def assign_name(self, name: str) -> str:
        if not name:
            logger.info("Name was not given. Please enter macro name...")
            while not name:
                name = Prompt.ask(PromptUtils.allow_abort("Please choose another name for the new macro"))
                UserOptions.check_if_abort_requested(name)
            return name.lower()
        return name.lower()

    def create_macro(self, path: str, name: str) -> None:
        try:
            extra_context = {
                "macro_name": name,
            }

            output = os.path.join(get_macros_dir(), path)
            cookiecutter(
                template=os.path.join(get_resources_dir(), "templates", "macros"),
                no_input=True,
                extra_context=extra_context,
                output_dir=output,
                overwrite_if_exists=False,
                skip_if_file_exists=False,
            )

            colored_model = PromptUtils.color_text(name, Logs.MODEL_HIGHLIGHT)
            logger.info(f"Macro {colored_model} successfully created in {path}. :white_check_mark:")
            logger.info(f"Model file can be found at {output}/{name}.sql")
            logger.info(f"Model metadata file can be found at {output}/{name}.yml")
        except OutputDirExistsException:
            logger.error("Macro already exists by that name. Please choose another name.")
