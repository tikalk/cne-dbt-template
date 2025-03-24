import logging
import os

import rich_click as click
from click_repl import repl
from dotenv import load_dotenv

from cli.utils.database.database_factory import get_database
from cli.utils.file_helper import get_root_dir
from cli.utils.prompt_abort_exception import PromptAbortException
from cli.utils.prompt_utils import (
    AppContext,
    prompt_kwargs,
    setup_repl_prompt,
    update_env_file,
)
from cli.utils.user_options import UserOptions

logger = logging.getLogger(__name__)


@click.group(help="Commands for selecting configuration vars (organization_id, organization_name, etc.)")
def select():
    """Commands for selecting configuration vars (organization_id, organization_name, etc.)"""
    pass


@select.command(help="Select organization data to work with")
def organization():
    """Commands for selecting organization data to work with"""
    try:
        load_dotenv(override=True)
        database = get_database()
        organization_table_name = "organization"
        columns_to_select = ["id", "display_name"]
        organizations_list = database.select_from_table(
            private_key_path=os.environ.get("SNOWFLAKE_PRIVATE_KEY_PATH"),
            account=os.environ.get("SNOWFLAKE_ACCOUNT"),
            user=os.environ.get("SNOWFLAKE_USERNAME"),
            warehouse=os.environ.get("SNOWFLAKE_WAREHOUSE"),
            database=os.environ.get("SOURCE_DATABASE"),
            schema="test_metadata",
            table_name=organization_table_name,
            columns=columns_to_select,
        )
        org_mapping_by_id = dict(organizations_list)
        org_mapping_by_name = {o_name: o_id for o_id, o_name in org_mapping_by_id.items()}
        org_names = [o_name for o_name in org_mapping_by_id.values()]
        organizations = UserOptions(org_names)
        selected_org = organizations.select("Please choose organization number / name to use")
        click.echo(f"Selected organization: {selected_org}")
        click.echo(f"selected org_id: {org_mapping_by_name[selected_org]}")

        update_env_file(f"{get_root_dir()}/.env", "ORG_NAME", selected_org)
        update_env_file(f"{get_root_dir()}/.env", "ORG_ID", org_mapping_by_name[selected_org])
        setup_repl_prompt()
        repl(AppContext().get_context(), prompt_kwargs=prompt_kwargs)

    except PromptAbortException as e:
        logger.info(e.message)
        return None
    except Exception as e:
        logger.error(str(e), e)
        return None
