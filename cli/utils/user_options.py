import logging
from typing import Optional

from rich.prompt import Prompt

from cli.const.constant import PromptKeywords
from cli.utils.prompt_abort_exception import PromptAbortException
from cli.utils.prompt_utils import PromptUtils

logger = logging.getLogger(__name__)


class UserOptions(object):
    def __init__(self, options: list, sort_options=True, allow_free_input: bool = False):
        self.options = options
        if sort_options:
            self.options = sorted(options)

        self.options_dict = {k: v for k, v in enumerate(self.options, 1)}
        self.allow_free_input = allow_free_input

    @staticmethod
    def check_if_abort_requested(input: str) -> None:
        if input.lower() == PromptKeywords.ABORT_KEYWORD.lower():
            raise PromptAbortException()

    @staticmethod
    def check_if_clear_requested(input: str) -> bool:
        return input.lower() == PromptKeywords.CLEAR_KEYWORD.lower()

    def get_options(self) -> list:
        return self.options

    def _promptAsk(self, prompt_message: str, default_selection: Optional[str] = None):
        result = Prompt.ask(prompt_message, default=default_selection)
        UserOptions.check_if_abort_requested(result)
        if UserOptions.check_if_clear_requested(result):
            result = None
        return result

    def _display_options(self):
        output = ""
        for key, value in self.options_dict.items():
            output += f"{key} -> {value}" + "\n"
        logger.info(output)

    def _select_internal(self, selection: str) -> Optional[str]:

        if not selection:
            return None

        UserOptions.check_if_abort_requested(selection)

        selection = selection.strip()
        if selection.isdigit():
            selection_as_digit = int(selection)
            if selection_as_digit in self.options_dict:
                selected_item = self.options_dict.get(selection_as_digit)
                logger.info(f"Selected {selection} for {selected_item}.\n\n")
                return selected_item
            elif self.allow_free_input:
                logger.info(f"Using free selection {selection}.")
                return selection
            else:
                logger.info(f"Selection {selection} is invalid -> Ignoring.")
                return None
        else:
            existing_values_lower = map(lambda dict_val: dict_val.lower(), self.options_dict.values())
            selected_lower = selection.lower()
            if selected_lower in existing_values_lower:
                logger.info(f"\nSelected {selected_lower}.\n\n")
                return selected_lower
            elif self.allow_free_input:
                logger.info(f"Using free selection {selection}.")
                return selection
            else:
                logger.info(f"Selection {selection} is invalid -> Ignoring.")
                return None

    def _build_message_for_user(self, message_for_user: str) -> str:
        if self.allow_free_input:
            if self._any_items_available():
                return f"{message_for_user} {PromptKeywords.FREE_TEXT_ALLOWED_SUFFIX}"
            else:
                return "No items available, please provide free text: "

        if self._any_items_available():
            return message_for_user

        return "No items available."

    def _validate_selection(self, selected_item: str) -> str:
        while selected_item is None:
            reselection_message = self._build_message_for_user("This is not a valid option. Please choose again")
            reselection = self._promptAsk(reselection_message)
            selected_item = self._select_internal(reselection)
        return selected_item

    def select(self, message_for_user: str, default_selection=None) -> str:
        selected_item = None
        while selected_item is None:
            if self._any_items_available():
                self._display_options()
            message_to_user = self._build_message_for_user(message_for_user)
            user_input = self._promptAsk(PromptUtils.allow_abort(message_to_user), default_selection)
            selected_item = self._select_internal(user_input)
            if selected_item:
                selected_item = str(selected_item)
        return str(self._validate_selection(selected_item))

    def select_multiple(self, message_for_user: str) -> list[str]:
        selections: list[str] = []
        if self._any_items_available():
            self._display_options()
        message_to_user = self._build_message_for_user(f"{message_for_user} - (Multiple selections allowed)")
        user_inputs = self._promptAsk(PromptUtils.allow_abort(message_to_user)).split(",")
        for input in user_inputs:
            input_selection = self._select_internal(input.strip())
            if input_selection:
                logger.debug(f"Added selection {input_selection}.")
                selections.append(str(self._select_internal(input.strip())))
        return selections

    def _any_items_available(self):
        return len(self.options) > 0
