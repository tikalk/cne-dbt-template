import logging

import rich_click as click

logger = logging.getLogger(__name__)


@click.group(help="Commands for updating objects (domain/model data tec.)")
def update():
    """Commands for updating objects (domain/model data tec.)"""
    pass


@update.command(help="Update model yml")
@click.option("-n", "--name", help="The name of the newly created model, must be in lowercase", type=str)
def model_yml(
    name: str,
) -> None:
    """Update model yml"""
    # database = get_database()
    pass
