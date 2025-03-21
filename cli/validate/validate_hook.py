import argparse
import logging
from typing import Optional, Sequence

from cli.utils.log_handlers import setup_log
from cli.validate.validate import validate_all

logger = logging.getLogger(__name__)


def main(argv: Optional[Sequence[str]] = None) -> int:
    """main method to invoke hook"""

    setup_log("DEBUG")
    logger.debug("validate hook")
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*", help="Filenames to check.")
    args = parser.parse_args(argv)
    comma_names = ", ".join(args.filenames)

    if validate_all(comma_names):
        return 0
    else:
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
