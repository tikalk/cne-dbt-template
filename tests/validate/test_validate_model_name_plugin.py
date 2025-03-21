import unittest

from cli.validate.validate_model_name_plugin import ModelNameValidatePlugin


class TestModelNameValidatePlugin(unittest.TestCase):

    def setUp(self):
        self.plugin = ModelNameValidatePlugin()

    def test_invalidate_valid_model(self):
        file_path_name = "models/domain/domain_model.sql"
        result = self.plugin.validate(file_path_name, None)
        self.assertFalse(result)

    def test_validate_valid_model(self):
        file_path_name = "models/collector/collector_slv__flatten_data.sql"
        result = self.plugin.validate(file_path_name, None)
        self.assertFalse(result)

    def test_validate_invalid_model_prefix(self):
        file_path_name = "models/domain/invalid_model.sql"

        result = self.plugin.validate(file_path_name, None)
        self.assertFalse(result)

    def test_validate_invalid_model_suffix(self):
        file_path_name = "models/domain/domain__model.sql"

        result = self.plugin.validate(file_path_name, None)
        self.assertFalse(result)

    def test_validate_model_not_in_staging_or_marts(self):
        file_path_name = "models/unknown/domain_model.sql"

        result = self.plugin.validate(file_path_name, None)
        self.assertFalse(result)

    def test_is_applicable(self):
        file_name = "models/domain_model.sql"

        result = self.plugin.is_applicable(file_name)
        self.assertTrue(result)

    def test_is_not_applicable(self):
        file_name = "not_models/domain_model.sql"

        result = self.plugin.is_applicable(file_name)
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
