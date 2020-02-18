#!/usr/bin/env python3


from typing import Tuple, NoReturn
from argparse import ArgumentParser
import sys


class ArgumentParserError(Exception):
    pass


class __ArgumentParser(ArgumentParser):
    """
    The method "error" has been redefined to achieve the following goals: (1) clearer application steps, and (2)
    to output errors in one style.
    1. By default, if an error is arisen during command-line arguments parsing, it just prints a preassigned error
    message, and the program is closed immediately with exit code 2. When the redefined method is used,
    the program raises the exception, that is processed in the main module "rooms_students" then.
    So, the entrance and exit from the application are handled in one module.
    2. By default error message looks as:
    execute:
      python rooms_db_accounting.py -s s.json
    stdout returns:
      usage: rooms_db_accounting [-h] -s STUDENTS -r ROOM [-f FORMAT]
      rooms_accounting: error: the following arguments are required: -r/--rooms
    When the redefined method is used, the clear message "the following arguments are required: -r/--rooms" goes
    throw the exception to the main function and prints there.
    """
    def error(self, message: str) -> NoReturn:
        raise ArgumentParserError(message)


def parse_command_line_args() -> Tuple[str, str, str]:
    """Parse args from the CLI and returns a tuple: (students: str, room: str, format: str)."""
    parser = __ArgumentParser(prog="rooms_db_accounting", description="Rooms accounting script.",
                              usage="rooms_db_accounting [-h] -s STUDENTS -r ROOM [-f FORMAT]")

    if len(sys.argv) == 1:
        parser.print_usage()
        parser.exit()

    parser.add_argument("-s", "--students",
                        metavar="STUDENTS",
                        type=str,
                        action="store",
                        dest="students_filename",
                        required=True,
                        help="input json file with students"
                        )

    parser.add_argument("-r", "--rooms",
                        metavar="ROOMS",
                        type=str,
                        action="store",
                        dest="rooms_filename",
                        required=True,
                        help="input json file with rooms"
                        )

    parser.add_argument("-f", "--format",
                        metavar="FORMAT",
                        type=str,
                        action="store",
                        dest="output_file_format",
                        required=False,
                        default="json",
                        help="output file format (json or xml; default = json)",
                        choices=("json", "xml")
                        )

    args = parser.parse_args()
    return args.students_filename, args.rooms_filename, args.output_file_format


if __name__ == "__main__":
    print("It is the CLI parsing module for rooms_db_accounting script.")
    try:
        students_filename, rooms_filename, output_file_format = parse_command_line_args()
    except ArgumentParserError as err:
        print(err)
    else:
        print("Output variables:\n"
              f"students_filename: {students_filename}\n"
              f"rooms_filename: {rooms_filename}\n"
              f"output_file_format: {output_file_format}")
