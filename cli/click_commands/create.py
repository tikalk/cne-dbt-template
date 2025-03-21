import logging
import os

import rich_click as click
from rich.prompt import Confirm, Prompt

from cli.commands.domain_command import DomainCommands
from cli.commands.macro_command import MacroCommands
from cli.commands.model_command import ModelCommands
from cli.const.const_model import ModelCode, ModelType
from cli.const.constant import Domains
from cli.utils.exceptions import CliException
from cli.utils.file_helper import get_folder_names, get_models_dir, list_files
from cli.utils.prompt_abort_exception import PromptAbortException
from cli.utils.prompt_utils import PromptUtils
from cli.utils.user_options import UserOptions

logger = logging.getLogger(__name__)

valid_model_type_names = ModelType.keys()
valid_model_code_type_names = ModelCode.keys()


@click.group(help="Commands for creating objects (domain/model data tec.)")
def create():
    """Commands for creating objects (domain/model data tec.)"""
    pass


@create.command(help="Create a new domain")
@click.argument("domain", nargs=1, required=False)
@click.option("-s", "--sub_domain", help="Sub Domain if relavent", type=str)
def domain(domain: str, sub_domain: str) -> None:
    """Create a new domain"""
    try:
        if not domain:
            domain = Prompt.ask(PromptUtils.allow_abort("Please enter a new domain name"))
            UserOptions.check_if_abort_requested(domain)
        if not sub_domain:
            if Confirm.ask("Do you want to create a sub domain?"):
                sub_domain = Prompt.ask(PromptUtils.allow_abort("Please enter a new sub domain name"))
                UserOptions.check_if_abort_requested(sub_domain)
        DomainCommands().create_domain(domain, sub_domain)

    except PromptAbortException as e:
        logger.info(e.message)


@create.command(help="Create a new integration tool")
@click.argument("tool_name", nargs=1, required=False)
@click.option("--asset/--no-asset", is_flag=True, default=True)
@click.option("--policy/--no-policy", is_flag=True, default=True)
def integration_tool(tool_name: str, asset: bool, policy: bool) -> None:
    """Create a new integration tool"""
    try:
        if not tool_name:
            tool_name = Prompt.ask(PromptUtils.allow_abort("Please enter a new Integration Tool name"))
            UserOptions.check_if_abort_requested(tool_name)
        DomainCommands().create_integration_tool(tool_name, asset, policy)

    except PromptAbortException as e:
        logger.info(e.message)


@create.command(help="Create a new silver/gold model")
@click.option("-d", "--domain", help="Domain to add the new model to", type=str)
@click.option("-tl", "--tool_name", help="Tool name if integration tool", type=str)
@click.option(
    "-t",
    "--type",
    help=f"Model type to create. Valid options are {valid_model_type_names}",
    type=click.Choice(valid_model_type_names, case_sensitive=False),
)
@click.option(
    "-c",
    "--code",
    help=f"Model code type to create. Valid options are {valid_model_code_type_names}",
    type=click.Choice(valid_model_code_type_names, case_sensitive=False),
    default="sql",
)
@click.option("-n", "--name", help="The name of the newly created model, must be in lowercase", type=str)
def model(
    domain: str,
    tool_name: str,
    type: str,
    code: str,
    name: str,
) -> None:
    """Create a new staging/mart model"""
    try:
        model_commands = ModelCommands()
        domain = DomainCommands().assign_domain(domain)
        if domain == Domains.TOOLS and not tool_name:
            tool_name = model_commands.assign_tool(tool_name)

        sub_domain_dir = os.path.join(get_models_dir(), domain)
        if not os.path.exists(sub_domain_dir):
            raise CliException(f"Folder {domain} does not exist")
        yml_files = list_files(sub_domain_dir, ".yml")
        if not yml_files:
            folder = get_folder_names(sub_domain_dir)
            folder_names = UserOptions(folder, sort_options=True)
            sub_folder = folder_names.select("Please choose type number / name to use")
            domain = os.path.join(domain, sub_folder)

        model_type: ModelType = model_commands.assign_type(type)
        model_code: ModelCode = model_commands.assign_code(code)
        name = model_commands.assign_name(domain, model_type, name, tool_name)
        model_commands.create_model(domain, model_type, model_code, name, tool_name)

    except PromptAbortException as e:
        logger.info(e.message)
        return None
    except Exception as e:
        logger.error(str(e), e)
        return None


@create.command(help="Create a new macro")
@click.option("-p", "--path", help="The folder path for the macro", type=str)
@click.option("-n", "--name", help="The name of the newly created macro, must be in lowercase", type=str)
def macro(
    path: str,
    name: str,
) -> None:
    """Create a new staging/mart model"""
    try:
        macro_commands = MacroCommands()
        path = macro_commands.assign_path(path)
        name = macro_commands.assign_name(name)
        macro_commands.create_macro(path, name)

    except PromptAbortException as e:
        logger.info(e.message)
        return None
    except Exception as e:
        logger.error(str(e), e)
        return None
