import unittest
from unittest.mock import patch

from cli.validate.validate_yaml_exists_plugin import YamlExistsValidatePlugin


class TestYamlExistsValidatePlugin(unittest.TestCase):
    def setUp(self):
        self.plugin = YamlExistsValidatePlugin()

    @patch("os.path.exists")
    @patch("cli.validate.validate_yaml_exists_plugin.ValidateSqlPlugin.get_full_file_name")
    def test_validate_yaml_exists(self, mock_get_full_file_name, mock_path_exists):
        mock_get_full_file_name.return_value = "test_file.yml"
        mock_path_exists.return_value = True

        result = self.plugin.validate("test_file.sql", None)
        self.assertTrue(result)
        mock_get_full_file_name.assert_called_once_with("test_file.yml")
        mock_path_exists.assert_called_once_with("test_file.yml")

    @patch("os.path.exists")
    @patch("cli.validate.validate_yaml_exists_plugin.ValidateSqlPlugin.get_full_file_name")
    @patch("cli.validate.validate_yaml_exists_plugin.logger")
    def test_validate_yaml_not_exists(self, mock_logger, mock_get_full_file_name, mock_path_exists):
        mock_get_full_file_name.return_value = "test_file.yml"
        mock_path_exists.return_value = False

        result = self.plugin.validate("test_file.sql", None)
        self.assertFalse(result)
        mock_get_full_file_name.assert_called_once_with("test_file.yml")
        mock_path_exists.assert_called_once_with("test_file.yml")
        mock_logger.error.assert_called_with("Model metadata missing file for test_file.yml")


if __name__ == "__main__":
    unittest.main()
