import logging
import os

import click
import snowflake.connector
from dotenv import load_dotenv

from cli.utils.database.database_base import DatabaseBase

load_dotenv()

logger = logging.getLogger(__name__)


class SnowflakeDB(DatabaseBase):
    def __init__(self):
        self.key_path: str = os.environ.get("SNOWFLAKE_PRIVATE_KEY_PATH", "")
        self.account: str = os.environ.get("SNOWFLAKE_ACCOUNT", "")
        self.user: str = os.environ.get("SNOWFLAKE_USERNAME", "")
        self.warehouse: str = os.environ.get("SNOWFLAKE_WAREHOUSE", "")

    # Function to connect to Snowflake and fetch the table definition
    def get_table_definition(self, database: str, schema: str, table_name: str):
        conn = snowflake.connector.connect(
            private_key_file=self.key_path, user=self.user, account=self.account, warehouse=self.warehouse, database=database, schema=schema
        )

        try:
            with conn.cursor() as cursor:
                cursor.execute(f"DESCRIBE TABLE {schema}.{table_name}")
                columns = cursor.fetchall()
        except Exception as e:
            logger.error(f"An error occurred: {e}")

        # Close the connection
        cursor.close()
        conn.close()

        # Return the columns as a dictionary
        return {col[0]: col[1] for col in columns}

    def select_from_table(self, database: str, schema: str, table_name: str, columns: list):
        conn = snowflake.connector.connect(
            self.key_path, user=self.user, account=self.account, warehouse=self.warehouse, database=database, schema=schema
        )
        formatted_string = ", ".join(f'"{col}"' for col in columns)
        query = f"SELECT {formatted_string} FROM {database}.{schema}.{table_name}"
        try:
            with conn.cursor() as cursor:
                cursor.execute(query)
                result_data = cursor.fetchall()
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            click.echo(f"An ERROR occurred: {str(e)}")
            click.echo(f"Please check that the schema and table exists in your db: {schema}.{table_name} ")
            raise e

        # Close the connection
        conn.close()

        return result_data
