import os
from abc import ABC

from cli.config import ini_config

home_dir = os.path.expanduser("~")
PERSIST_FOLDER = home_dir + "/." + ini_config.get("cli", "log_file_folder", fallback="cli")


class PromptKeywords(ABC):
    ABORT_KEYWORD = "ABORT"
    CLEAR_KEYWORD = "CLEAR"
    FREE_TEXT_ALLOWED_SUFFIX = " :point_right: You can use free text as well! :point_left:"
    PROMPT_COLOR = "#00e6e6"


class FileTypes(ABC):
    SQL = ".sql"
    YML = ".yml"
    MD = ".md"


class FileNames(ABC):
    DBT_PROJECT_FILE = "dbt_project.yml"


class Logs(ABC):
    RIGHT_ARROW = ":point_right:"
    MODEL_HIGHLIGHT = "green bold"


class Domains(ABC):
    TOOLS = "tools"
