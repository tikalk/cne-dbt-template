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


@click.group(help="Lean more about dbt")
def learn():
    """Commands imported from task files"""
    pass


@learn.command(help="View catalog documentation")
def catalog():
    """View catalog documentation"""
    click.launch("https://docs.getdbt.com/reference/artifacts/catalog-json")

@learn.command(help="Learn more about dbt")
def dbt_info():
    """Learn more about dbt"""
    click.launch("https://learn.getdbt.com/catalog?labels=%5B%22dbt%20Experience%22%5D&values=%5B%22New%20to%20dbt%22%5D")
