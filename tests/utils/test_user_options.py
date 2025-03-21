import unittest
from unittest import mock

from cli.const.constant import PromptKeywords
from cli.utils.prompt_abort_exception import PromptAbortException
from cli.utils.user_options import UserOptions


class TestUserOptions(unittest.TestCase):

    @mock.patch("cli.utils.user_options.Prompt.ask")
    @mock.patch("cli.utils.user_options.PromptUtils.allow_abort")
    def test_select_valid_option(self, mock_allow_abort, mock_prompt_ask):
        options = ["option1", "option2", "option3"]
        user_options = UserOptions(options)
        mock_allow_abort.side_effect = lambda x: x
        mock_prompt_ask.return_value = "1"

        result = user_options.select("Choose an option")

        self.assertEqual(result, "option1")

    @mock.patch("cli.utils.user_options.Prompt.ask")
    @mock.patch("cli.utils.user_options.PromptUtils.allow_abort")
    def test_select_invalid_option(self, mock_allow_abort, mock_prompt_ask):
        options = ["option1", "option2", "option3"]
        user_options = UserOptions(options)
        mock_allow_abort.side_effect = lambda x: x
        mock_prompt_ask.side_effect = ["4", "1"]

        result = user_options.select("Choose an option")

        self.assertEqual(result, "option1")

    @mock.patch("cli.utils.user_options.Prompt.ask")
    @mock.patch("cli.utils.user_options.PromptUtils.allow_abort")
    def test_select_free_input_allowed(self, mock_allow_abort, mock_prompt_ask):
        options = ["option1", "option2", "option3"]
        user_options = UserOptions(options, allow_free_input=True)
        mock_allow_abort.side_effect = lambda x: x
        mock_prompt_ask.return_value = "free_input"

        result = user_options.select("Choose an option")

        self.assertEqual(result, "free_input")

    @mock.patch("cli.utils.user_options.Prompt.ask")
    @mock.patch("cli.utils.user_options.PromptUtils.allow_abort")
    def test_select_abort_requested(self, mock_allow_abort, mock_prompt_ask):
        options = ["option1", "option2", "option3"]
        user_options = UserOptions(options)
        mock_allow_abort.side_effect = lambda x: x
        mock_prompt_ask.return_value = PromptKeywords.ABORT_KEYWORD

        with self.assertRaises(PromptAbortException):
            user_options.select("Choose an option")

    @mock.patch("cli.utils.user_options.Prompt.ask")
    @mock.patch("cli.utils.user_options.PromptUtils.allow_abort")
    def test_select_clear_requested(self, mock_allow_abort, mock_prompt_ask):
        options = ["option1", "option2", "option3"]
        user_options = UserOptions(options)
        mock_allow_abort.side_effect = lambda x: x
        mock_prompt_ask.side_effect = [PromptKeywords.CLEAR_KEYWORD, "1"]

        result = user_options.select("Choose an option")

        self.assertEqual(result, "option1")


if __name__ == "__main__":
    unittest.main()
