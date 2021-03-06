#!/usr/bin/env python3
"""
yes, this is python 3 ONLY project
"""
import sys
import argparse
import logging

from sen import set_logging
from sen.exceptions import TerminateApplication
from sen.tui.init import UI
from sen.util import setup_dirs, get_log_file_path

logger = logging.getLogger("sen")


def main():
    parser = argparse.ArgumentParser(
        description="Terminal User Interface for Docker Engine"
    )
    exclusive_group = parser.add_mutually_exclusive_group()
    exclusive_group.add_argument("--debug", action="store_true", default=None)

    args = parser.parse_args()

    # if args.debug:
    set_logging(level=logging.DEBUG, path=get_log_file_path())
    # else:
    #     set_logging(level=logging.INFO, path=setup_dirs())

    logger.info("application started")

    try:
        ui = UI()
    except TerminateApplication as ex:
        print("Error: {0}".format(str(ex)), file=sys.stderr)
        return 1

    try:
        ui.run()
    except KeyboardInterrupt:
        print("Quitting on user request.")
        return 1
    except Exception as ex:  # pylint: disable=broad-except
        if args.debug:
            raise
        else:
            logger.error("Exception caught: %r", ex)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
