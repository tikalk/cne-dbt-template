import logging
import os
import shutil
import subprocess

import rich_click as click

from cli.const.const_model import ModelType
from cli.utils.file_helper import get_root_dir

logger = logging.getLogger(__name__)

valid_model_type_names = ModelType.keys()


@click.group(help="Commands for log debugging")
def log():
    """Commands for log debugging"""
    pass


@log.command(help="Delete log files")
def clean() -> None:
    """Delete log files"""
    shutil.rmtree(get_root_dir() + "/logs")
    click.echo("Logs deleted")


@log.command(help="Open Log file")
def open() -> None:
    """Open Log file"""
    log_file = get_root_dir() + "/logs/dbt.log"
    env = os.environ.copy()
    subprocess.run(["code", log_file], env=env, check=True)
