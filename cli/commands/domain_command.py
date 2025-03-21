import logging
import os
import shutil
from abc import ABC
from typing import Optional

from cookiecutter.main import cookiecutter

from cli.commands.model_command import ModelCommands
from cli.const.const_model import ModelType
from cli.const.constant import Logs
from cli.utils.file_helper import get_models_dir, get_resources_dir
from cli.utils.prompt_utils import PromptUtils
from cli.utils.user_options import UserOptions

logger = logging.getLogger(__name__)


class DomainCommands(ABC):
    def create_domain(self, domain: str, sub_domain: Optional[str]):
        self._create_domain_folders(domain, sub_domain)

    def _get_domain_name(self, path: str):
        relative_path = path.replace(get_models_dir(), "")
        if not relative_path.startswith("/tools"):
            return relative_path.split("/")[1]
        return relative_path.split("/")[2]

    def _create_domain_folders(self, domain: str, sub_domain: Optional[str]):  ## check if domain folder exists
        domain_dir = os.path.join(get_models_dir(), domain, *(filter(None, [sub_domain])))

        if domain_dir.startswith(get_models_dir()):
            if os.path.exists(domain_dir):
                raise Exception(f"Domain {domain} already exists")

            domain_template = os.path.join(get_resources_dir(), "templates", "domain")

            if sub_domain:
                outout_dir = os.path.join(get_models_dir(), domain)
                extra_context = {
                    "domain_name": sub_domain,
                }
            else:
                outout_dir = get_models_dir()
                extra_context = {
                    "domain_name": domain,
                }

            cookiecutter(
                template=domain_template,
                checkout=None,
                no_input=True,
                extra_context=extra_context,
                replay=None,
                overwrite_if_exists=True,
                output_dir=outout_dir,
                config_file=None,
                default_config=False,
                password=None,
                directory=None,
                skip_if_file_exists=False,
                accept_hooks=True,
            )
            colored_domain = PromptUtils.color_text("/".join(filter(None, [domain, sub_domain])), Logs.MODEL_HIGHLIGHT)
            logger.info(f"Domain {colored_domain} successfully Created. :white_check_mark:")

    def create_integration_tool(self, tool_name: str, asset: bool, policy: bool) -> None:
        """Creates a new integration tool for the specified domain."""
        tool_dir = os.path.join(get_models_dir(), "tools")
        tool_named_dir = os.path.join(get_models_dir(), "tools", tool_name)

        if tool_named_dir.startswith(get_models_dir()):
            if os.path.exists(tool_named_dir):
                raise Exception(f"Domain {tool_named_dir} already exists")

            domain_template = os.path.join(get_resources_dir(), "templates", "tool")

            extra_context = {
                "tool_name": tool_name,
                "create_asset": asset,
                "create_policy": policy,
            }

            cookiecutter(
                template=domain_template,
                checkout=None,
                no_input=True,
                extra_context=extra_context,
                replay=None,
                overwrite_if_exists=True,
                output_dir=tool_dir,
                config_file=None,
                default_config=False,
                password=None,
                directory=None,
                skip_if_file_exists=False,
                accept_hooks=True,
            )

            model_prefix = ModelType.get_model_prefix(ModelType.STAGING)
            if not asset:
                ## delete asset folder
                asset_dir = os.path.join(tool_named_dir, ModelCommands()._get_staging_compatible_folder(), f"{tool_name}_{model_prefix}__asset")
                if os.path.exists(asset_dir):
                    shutil.rmtree(asset_dir)
            if not policy:
                ## delete asset folder

                policy_dir = os.path.join(tool_named_dir, ModelCommands()._get_staging_compatible_folder(), f"{tool_name}_{model_prefix}__policy")
                if os.path.exists(policy_dir):
                    shutil.rmtree(policy_dir)
            colored_domain = PromptUtils.color_text(tool_name, Logs.MODEL_HIGHLIGHT)
            logger.info(f"Integration tool {colored_domain} successfully Created. :white_check_mark:")

    def assign_domain(self, domain: str) -> str:
        if not domain:
            logger.info("Domain type not given. Loading available types...")
            items = os.listdir(get_models_dir())
            folders = [item for item in items if os.path.isdir(os.path.join(get_models_dir(), item))]
            types = UserOptions(folders)
            selected_type = types.select("Please choose type number / name to use")
            return selected_type
        return domain
