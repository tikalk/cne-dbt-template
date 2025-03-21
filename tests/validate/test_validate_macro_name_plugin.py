import unittest

from cli.validate.validate_macro_name_plugin import MacroNameValidatePlugin


class TestMacroNameValidatePlugin(unittest.TestCase):

    def setUp(self):
        self.plugin = MacroNameValidatePlugin()

    def test_is_applicable_sql_file(self):
        file_name = "macro_test.sql"
        self.assertFalse(self.plugin.is_applicable(file_name))
        file_name = "macros/test.sql"
        self.assertTrue(self.plugin.is_applicable(file_name))

    def test_is_applicable_yml_file(self):
        file_name = "macro_test.yml"
        self.assertFalse(self.plugin.is_applicable(file_name))
        file_name = "macros/test.yml"
        self.assertTrue(self.plugin.is_applicable(file_name))

    def test_is_applicable_non_macro_sql_file(self):
        file_name = "test.sql"
        self.assertFalse(self.plugin.is_applicable(file_name))

    def test_is_applicable_non_macro_yml_file(self):
        file_name = "test.yml"
        self.assertFalse(self.plugin.is_applicable(file_name))

    def test_is_applicable_non_sql_yml_file(self):
        file_name = "macro_test.txt"
        self.assertFalse(self.plugin.is_applicable(file_name))


if __name__ == "__main__":
    unittest.main()
