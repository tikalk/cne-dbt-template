import json
import logging
import os
import pathlib
import sys
import traceback

import ccl
import rich_click as click
from click_repl import repl
from dbt_artifacts_parser.parser import parse_manifest_v12, parse_run_results_v6
from dbt_artifacts_parser.parsers.run_results.run_results_v6 import Status
from rich.prompt import Prompt

from cli.commands.model_command import ModelCommands
from cli.config import ini_config
from cli.const.const_model import ModelType
from cli.go_tasks import GoTasks, tasks
from cli.utils.database.database_factory import get_database
from cli.utils.file_helper import get_models_dir, get_root_dir, get_target_dir
from cli.utils.log_handlers import setup_log, setup_logger
from cli.utils.prompt_utils import (
    AppContext,
    PromptUtils,
    prompt_kwargs,
    setup_repl_prompt,
)
from cli.validate.validate import validate

# Use Rich markup
click.rich_click.USE_RICH_MARKUP = True

logger = logging.getLogger(__name__)


@click.group(help="Commands for creating objects (domain/model data ect.)")
def cli():
    """Commands for creating objects (domain/model data ect.)"""
    pass


@cli.command(help="""Show cli history commands""")
@click.option("-l", "--limit", default=-1, help="History Limit", type=int)
def history(limit: int):
    """Show cli history commands"""
    history_lines = prompt_kwargs["history"].get_strings()
    count_lines = 0
    for line in history_lines:
        count_lines = count_lines + 1
        if limit != -1 and count_lines > limit:
            break
        click.echo(line)


@cli.command(help="Exit")
def exit():
    """Exit"""
    os._exit(0)


@cli.command(help="Start")
def start():
    setup_log("INFO")
    setup_logger(logger, "INFO")

    file_path = f"{get_root_dir()}/ascii_art.txt"
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            logger.info(PromptUtils.color_text(line.strip(), "dark_green"))

    logger.info("\n\n")
    logger.info(ini_config.get("gui", "startup_logo", fallback="Welcome to the dbt CLI"))

    setup_repl_prompt()
    AppContext().set_context(click.get_current_context())
    repl(AppContext().get_context(), prompt_kwargs=prompt_kwargs)


def tasks_callback(task_name: str):
    if task_name in ["dbt:run-slim", "dbt:run"]:

        base_custom_name = ModelType.get_model_prefix(ModelType.BASE)
        staging_custom_name = ModelType.get_model_prefix(ModelType.STAGING)

        database = get_database()
        with open(f"{get_target_dir()}/run_results.json", "r") as fp_results, open(f"{get_target_dir()}/manifest.json", "r") as fp_manifest:
            try:
                run_results_dict = json.load(fp_results)
                run_results_obj = parse_run_results_v6(run_results=run_results_dict)
                manifest_dict = json.load(fp_manifest)
                manifest_obj = parse_manifest_v12(manifest=manifest_dict)

                success_results = [x for x in run_results_obj.results if x.status == Status.success]
                total_models = len(success_results)

                for index, result in enumerate(success_results):
                    unique_id = result.unique_id
                    if unique_id.startswith("model."):
                        node = manifest_obj.nodes[unique_id]

                        column_definitions = database.get_table_definition(
                            node.database,
                            node.schema_,
                            node.name.replace(f"_{staging_custom_name}", "").replace(f"_{base_custom_name}", ""),
                        )
                        model_commands = ModelCommands()
                        model_type = model_commands.get_model_type_by_dir(node.path)
                        model_access = model_commands.get_access_by_type(model_type)

                        root, _ = os.path.splitext(os.path.join(get_models_dir(), node.path))
                        yml_file = root + ".yml"
                        node_path = node.path.split("/")[0]
                        if node_path == "tools":
                            node_path = node.path.split("/")[1]
                        group = node_path
                        logger.info(f"{index} of {total_models}: Updating model: {node.name} yaml")
                        database.update_dbt_yaml(yml_file, node.name, column_definitions, model_access, group)
            except Exception as e:
                logger.error(f"Error updating dbt yaml: {e}")
    elif task_name in [
        "dbt:set-source-production-eu",
        "dbt:set-source-production-us",
        "dbt:set-source-staging",
        "dbt:set-source-local",
        "dbt:enable-slim",
        "dbt:disable-slim",
    ]:
        setup_repl_prompt()
        repl(AppContext().get_context(), prompt_kwargs=prompt_kwargs)


def setup_commands():

    path_to_commands = pathlib.Path(__file__, "..", "click_commands")
    ccl.register_commands(cli, path_to_commands)

    GoTasks().set_callback(tasks_callback)
    GoTasks().generate_go_tasks()
    cli.add_command(validate)
    cli.add_command(tasks)


setup_commands()


def log_exception(exc_type, exc_value, exc_traceback):
    """handle all exceptions"""
    filename, line, dummy, dummy = traceback.extract_tb(exc_traceback).pop()
    filename = os.path.basename(filename)
    error = "%s: %s" % (exc_type.__name__, exc_value)
    logger.error(":woman_facepalming: " + error)
    logger.error(f"filename: {filename} : {line}")
    logger.error(traceback.format_exc())
    Prompt.ask("Press key to exit.")


sys.excepthook = log_exception

if __name__ == "__main__":
    cli()
