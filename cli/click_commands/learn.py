import logging

import rich_click as click


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
