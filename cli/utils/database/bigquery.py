import logging
import os

from dotenv import load_dotenv
from google.cloud import bigquery
from google.oauth2 import service_account

from cli.utils.database.database_base import DatabaseBase

load_dotenv()

logger = logging.getLogger(__name__)


class BigqueryDB(DatabaseBase):
    def __init__(self):
        self.key_path: str = os.environ.get("BIGQUERY_KEYFILE_PATH", "")
        self.account: str = os.environ.get("DBT_PROFILE_PROJECT", "")
        self.user: str = os.environ.get("BIGQUERY_USERNAME", "")
        self.database: str = os.environ.get("BIGQUERY_DATABASE", "")

    # Function to connect to Snowflake and fetch the table definition
    def get_table_definition(self, database: str | None, schema: str | None, table_name: str | None):
        credentials = service_account.Credentials.from_service_account_file(self.key_path)

        # Create BigQuery client
        client = bigquery.Client(credentials=credentials, project=self.account)

        try:
            # Get table reference
            table_ref = client.dataset(schema).table(table_name)
            # Get table object
            table = client.get_table(table_ref)
            # Get schema
            table_schema = table.schema
            return {field.name: field.field_type for field in table_schema}
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            raise e

    def select_from_table(self, schema, table_name: str, columns: list):

        return None
