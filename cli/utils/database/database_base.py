from abc import ABC

import yaml

from cli.commands.domain_command import DomainCommands
from cli.commands.model_command import ModelCommands
from cli.const.const_model import ModelType


class DatabaseBase(ABC):
    column_order = ["name", "description", "type"]  # Adjust based on your preference

    def get_table_definition(
        self,
        database: str | None,
        schema: str | None,
        table_name: str | None,
    ):
        pass

    # Function to update the DBT model's YAML file with the new columns
    def update_dbt_yaml(self, yml_file_path, model_name, column_definitions, access, group):
        try:
            with open(yml_file_path, "r") as file:
                yml_data = yaml.safe_load(file)
        except FileNotFoundError:
            yml_data = {}

        # Check if the model exists, if not, create it
        if not yml_data:
            yml_data = {"models": [{"name": model_name, "description": "[Add description here]", "columns": []}]}
        if "models" not in yml_data:
            yml_data["models"] = []

        model_exists = False
        for model in yml_data["models"]:
            if model.get("name") == model_name:
                model_exists = True
                break

        if not model_exists:
            yml_data["models"].append({"name": model_name, "description": "[Add description here]", "columns": []})

        # Find the model and update the columns section
        for model in yml_data["models"]:
            if model.get("name") == model_name:
                if "config" not in model:
                    model["config"] = {}
                config = model["config"]
                config["group"] = group
                if "tags" not in model:
                    model["tags"] = []
                model_type = ModelCommands().get_model_type_by_dir(yml_file_path).get_layer_name()
                domain_name = DomainCommands()._get_domain_name(yml_file_path).lower()
                if "tags" not in config:
                    config["tags"] = []

                for mode_type in ModelType.get_model_valid_types():
                    layer = mode_type.get_layer_name()
                    if layer in config["tags"]:
                        config["tags"].remove(layer)
                if model_type not in config["tags"]:
                    config["tags"].append(model_type)
                if domain_name not in config["tags"]:
                    config["tags"].append(domain_name)
                model["access"] = access
                model_columns = model.get("columns", [])
                for col_name, col_type in column_definitions.items():
                    # Check if column is already in the model, if not add it
                    if not any(col["name"] == col_name for col in model_columns):
                        model_columns.append({"name": col_name, "type": col_type, "description": "[Add description here]"})
                model["columns"] = model_columns

        # Write the updated YAML file
        with open(yml_file_path, "w") as file:
            yaml.dump(yml_data, file, default_flow_style=False, sort_keys=False)

    def select_from_table(self, private_key_path, account, user, warehouse, database, schema, table_name: str, columns: list):
        pass
