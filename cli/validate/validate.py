import logging

import rich_click as click

from cli.validate.validate_command import ValidateCommand
from cli.validate.validate_decorators import filenames_option
from cli.validate.validate_macro_name_plugin import MacroNameValidatePlugin
from cli.validate.validate_model_name_plugin import ModelNameValidatePlugin
from cli.validate.validate_yaml_exists_plugin import YamlExistsValidatePlugin

logger = logging.getLogger(__name__)


def validate_all(filenames: str) -> int:
    try:
        return ValidateCommand().validate_files(
            filenames,
            [
                YamlExistsValidatePlugin(),
                ModelNameValidatePlugin(),
                MacroNameValidatePlugin(),
                # ModelValidatePlugin(),
                # SourceValidatePlugin(),
                # ValidateSqlSyntaxPlugin(),
            ],
        )
    except Exception as e:
        logger.error(e)
        return -1


@click.command(help="Execute all existing validations")
@filenames_option()
def all(filenames):
    """Execute all existing validations"""
    if validate_all(filenames):
        logger.info("All files are valid.")


@click.group(help="Commands for configuration validation")
def validate():
    """Commands for configuration validation"""
    pass


validate.add_command(all)
