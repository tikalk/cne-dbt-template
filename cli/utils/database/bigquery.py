import logging

from dotenv import load_dotenv
from google.cloud import bigquery
from google.oauth2 import service_account

from cli.utils.database.database_base import DatabaseBase

load_dotenv()

logger = logging.getLogger(__name__)


class BigqueryDB(DatabaseBase):

    # Function to connect to Snowflake and fetch the table definition
    def get_table_definition(self, private_key_path: str, account: str, user: str, warehouse: str, database: str, schema: str, table_name: str):
        credentials = service_account.Credentials.from_service_account_file(private_key_path)

        # Create BigQuery client
        client = bigquery.Client(credentials=credentials, project=account)

        try:
            # Get table reference
            table_ref = client.dataset(schema).table(table_name)
            # Get table object
            table = client.get_table(table_ref)
            # Get schema
            schema = table.schema
            return {field.name: field.field_type for field in schema}
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            raise e

    def select_from_table(self, private_key_path, account, user, warehouse, database, schema, table_name: str, columns: list):

        return None
