import unittest
from unittest.mock import MagicMock, patch

from cli.validate.validate_command import ValidateCommand
from cli.validate.validate_plugin import ValidatePlugin


class TestValidateCommand(unittest.TestCase):
    @patch("cli.validate.validate_command.get_root_dir", return_value="/root/dir")
    def test_validate_files_all_valid(self, mock_get_root_dir):
        validator_mock = MagicMock(spec=ValidatePlugin)
        validator_mock.is_applicable.return_value = True
        validator_mock.load_file.return_value = {"key": "value"}
        validator_mock.validate.return_value = True

        validate_command = ValidateCommand()
        result = validate_command.validate_files("file1.yml,file2.sql", [validator_mock])

        self.assertTrue(result)
        validator_mock.is_applicable.assert_called()
        validator_mock.load_file.assert_called()
        validator_mock.validate.assert_called()

    @patch("cli.validate.validate_command.get_root_dir", return_value="/root/dir")
    def test_validate_files_some_invalid(self, mock_get_root_dir):
        validator_mock = MagicMock(spec=ValidatePlugin)
        validator_mock.is_applicable.side_effect = [True, True]
        validator_mock.load_file.side_effect = [{"key": "value"}, {"key": "value"}]
        validator_mock.validate.side_effect = [True, False]

        validate_command = ValidateCommand()
        result = validate_command.validate_files("file1.yml,file2.sql", [validator_mock])

        self.assertFalse(result)
        validator_mock.is_applicable.assert_called()
        validator_mock.load_file.assert_called()
        validator_mock.validate.assert_called()

    @patch("cli.validate.validate_command.get_root_dir", return_value="/root/dir")
    def test_validate_files_not_applicable(self, mock_get_root_dir):
        validator_mock = MagicMock(spec=ValidatePlugin)
        validator_mock.is_applicable.return_value = False

        validate_command = ValidateCommand()
        result = validate_command.validate_files("file1.yml,file2.sql", [validator_mock])

        self.assertTrue(result)
        validator_mock.is_applicable.assert_called()
        validator_mock.load_file.assert_not_called()
        validator_mock.validate.assert_not_called()


if __name__ == "__main__":
    unittest.main()
