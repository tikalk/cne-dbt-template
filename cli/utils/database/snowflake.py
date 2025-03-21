import logging

import click
import snowflake.connector
from dotenv import load_dotenv

from cli.utils.database.database_base import DatabaseBase

load_dotenv()

logger = logging.getLogger(__name__)


class SnowflakeDB(DatabaseBase):

    # Function to connect to Snowflake and fetch the table definition
    def get_table_definition(self, sf_private_key_path, sf_account, sf_user, sf_warehouse, sf_database, sf_schema, table_name):
        conn = snowflake.connector.connect(
            private_key_file=sf_private_key_path, user=sf_user, account=sf_account, warehouse=sf_warehouse, database=sf_database, schema=sf_schema
        )

        try:
            with conn.cursor() as cursor:
                cursor.execute(f"DESCRIBE TABLE {sf_schema}.{table_name}")
                columns = cursor.fetchall()
        except Exception as e:
            logger.error(f"An error occurred: {e}")

        # Close the connection
        cursor.close()
        conn.close()

        # Return the columns as a dictionary
        return {col[0]: col[1] for col in columns}

    def select_from_table(self, sf_private_key_path, sf_account, sf_user, sf_warehouse, sf_database, sf_schema, table_name: str, columns: list):
        conn = snowflake.connector.connect(
            private_key_file=sf_private_key_path, user=sf_user, account=sf_account, warehouse=sf_warehouse, database=sf_database, schema=sf_schema
        )
        formatted_string = ", ".join(f'"{col}"' for col in columns)
        query = f"SELECT {formatted_string} FROM {sf_database}.{sf_schema}.{table_name}"
        try:
            with conn.cursor() as cursor:
                cursor.execute(query)
                result_data = cursor.fetchall()
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            click.echo(f"An ERROR occurred: {str(e)}")
            click.echo(f"Please check that the schema and table exists in your db: {sf_schema}.{table_name} ")
            raise e

        # Close the connection
        conn.close()

        return result_data
