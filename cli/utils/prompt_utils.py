import os

from dotenv import load_dotenv
from prompt_toolkit.history import FileHistory
from prompt_toolkit.styles import Style
from singleton_decorator import singleton

from cli.config import ini_config
from cli.const.constant import PERSIST_FOLDER, PromptKeywords


@singleton
class AppContext:
    def __init__(self):
        self.start_context = None

    def set_context(self, context):
        self.start_context = context

    def get_context(self):
        return self.start_context


style = Style.from_dict(
    {
        "": PromptKeywords.PROMPT_COLOR,
    }
)
prompt_kwargs = {
    "history": FileHistory(os.path.expanduser(PERSIST_FOLDER + "/.repl_history")),
    "message": "> ",
    "style": style,
}


def update_env_file(env_file: str, key: str, value: str):
    """
    Update or add a key-value pair in a .env file.

    :param env_file: Path to the .env file
    :param key: The key to update or add
    :param value: The value to set
    """
    env_lines = []
    key_exists = False

    # Read the existing .env file
    if os.path.exists(env_file):
        with open(env_file, "r") as file:
            env_lines = file.readlines()

        # Update the key if it exists
        for i, line in enumerate(env_lines):
            if line.startswith(f"{key}="):
                env_lines[i] = f"{key}={value}\n"
                key_exists = True
                break

    # Add the key if it doesn't exist
    if not key_exists:
        env_lines.append(f"{key}={value}\n")

    # Write back to the .env file
    with open(env_file, "w") as file:
        file.writelines(env_lines)


def setup_repl_prompt():
    load_dotenv(override=True)
    os.makedirs(PERSIST_FOLDER, exist_ok=True)
    prompt = ini_config.get("cli", "prompt", fallback="cli> ")
    db = os.getenv("SOURCE_DATABASE", None)
    org = os.getenv("ORG_NAME", None)

    db_params = f"{db}" if db else None
    org_params = f":{org}" if org else None
    extra_params = "".join(filter(None, [db_params, org_params]))
    prompt_kwargs["message"] = f"[{extra_params}] {prompt} "
    # generate_go_tasks()
    # internal_repl(
    #         click.get_current_context(),
    #         prompt_kwargs=prompt_kwargs,
    #     )


class PromptUtils(object):
    @staticmethod
    def allow_abort(text: str) -> str:
        return f"{text}, '[thistle1]{PromptKeywords.ABORT_KEYWORD}[/thistle1]' to cancel"

    @staticmethod
    def allow_clear(text: str) -> str:
        return f"{text}, '[thistle1]{PromptKeywords.CLEAR_KEYWORD}[/thistle1]' to clear"

    @staticmethod
    def color_text(text, color) -> str:
        return f"[{color}]{text}[/{color}]"

    @staticmethod
    def color_red(text: str) -> str:
        return PromptUtils.color_text(text, "red")
