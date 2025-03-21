import os

from cli.utils.database.database_base import DatabaseBase
from cli.utils.database.snowflake import SnowflakeDB


def get_database() -> DatabaseBase:
    if os.environ.get("DATABASE_TYPE", "SNOWFLAKE") == "SNOWFLAKE":
        return SnowflakeDB()
    else:
        raise ValueError("Database type not supported")
