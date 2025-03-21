import logging
import os

from cli.const.constant import FileTypes
from cli.validate.validate_sql_plugin import ValidateSqlPlugin

logger = logging.getLogger(__name__)


class YamlExistsValidatePlugin(ValidateSqlPlugin):
    def validate(self, file_name: str, data: object) -> bool:
        try:
            yml_filename = self.get_full_file_name(file_name.strip().replace(FileTypes.SQL, FileTypes.YML))
            if not os.path.exists(yml_filename):
                file_name = os.path.basename(yml_filename.replace("\\", os.sep))
                logger.error(f"Model metadata missing file for {file_name}")
                model_name = file_name.replace(FileTypes.SQL, "")
                logger.info(f"run: koalas_cli model field-enhance -m {model_name}")
                return False
            return True
        except Exception as e:
            logger.error("YamlExistsValidatePlugin ", e)
            return False
