import typing as t

import rich_click as click
from click.core import Option as Option
from click.decorators import FC, _param_memo


def build_option(f, param_decls, option_attrs):
    OptionClass = option_attrs.pop("cls", Option)
    _param_memo(f, OptionClass(param_decls, **option_attrs))
    return f


def filenames_option() -> t.Callable[[FC], FC]:
    def decorator(f: FC) -> FC:
        return build_option(
            f,
            ("-f", "--filenames"),
            {"default": "", "is_flag": False, "help": "Sets target filenames", "metavar": "<filenames>", "type": click.STRING},
        )

    return decorator
