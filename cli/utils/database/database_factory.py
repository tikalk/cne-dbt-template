from cli.config import ini_config
from cli.utils.database.bigquery import BigqueryDB
from cli.utils.database.database_base import DatabaseBase
from cli.utils.database.snowflake import SnowflakeDB


def get_database() -> DatabaseBase:
    if ini_config.get("dbt", "database_type", fallback="SNOWFLAKE") == "SNOWFLAKE":
        return SnowflakeDB()
    elif ini_config.get("dbt", "database_type", fallback="SNOWFLAKE") == "BIGQUERY":
        return BigqueryDB()
    else:
        raise ValueError("Database type not supported")
