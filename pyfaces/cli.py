################################################################################
#
#    Copyright 2020-2022 @ Félix Brezo (@febrezo)
#
#    This program is part of Pyfaces. You can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################

import argparse
import concurrent.futures
import json
import pathlib
import sys
import time

import pyfaces
import pyfaces.misc.text as text
from pyfaces.misc.colors import emphasis
from pyfaces.misc.colors import error
from pyfaces.misc.colors import success
from pyfaces.misc.colors import title
from pyfaces.misc.colors import warning
from pyfaces.core.processor import FaceProcessor
from pyfaces.core.configuration import ConfigManager


def get_parser():
    """Defines the argument parser
    Returns:
        argparse.ArgumentParser.
    """
    config = ConfigManager()

    parser = argparse.ArgumentParser(
        description= 'Pyfaces CLI | A face recognition tool to make it accesible for everyone and learn from it to what extent we are exposed.',
        prog='pyfaces',
        add_help=False,
        conflict_handler='resolve'
    )

    # Add subcommands as subparsers.
    subcommands = parser.add_subparsers(
        title="SUBCOMMANDS",
        description="List of available commands that can be invoked using Pyfaces CLI.",
        metavar="<sub_command> <sub_command_options>",
        dest='command_name'
    )

    compare_parser = argparse.ArgumentParser(
        description='A parser to manage comparisons between faces',
        prog='compare',
        epilog="",
        add_help=False,
        conflict_handler='resolve'
    )

    compare_parser.add_argument('face_path_1', metavar='<PATH>', action='store', help='The path to the extracted face.')
    compare_parser.add_argument('face_path_2', metavar='<PATH>', action='store', help='The path to the extracted face.')
    compare_parser.add_argument('--force-recalculation', default=False, action='store_true', help='Force recalculation of operations. Default: False.')

    compare_group_about = compare_parser.add_argument_group('About arguments', 'Showing additional information about this program.')
    compare_group_about.add_argument('-h', '--help', action='help', help='shows this help and exists.')
    compare_group_about.add_argument('--version', action='version', version=f'[%(prog)s] Pyfaces {pyfaces.__version__}', help='shows the version of the program and exits.')

    subparser_alias_generator = subcommands.add_parser(
        "compare",
        help="Compare two face files",
        parents=[compare_parser]
    )

    extract_parser = argparse.ArgumentParser(
        description='A parser to extract faces from images',
        prog='extract',
        epilog="",
        add_help=False,
        conflict_handler='resolve'
    )

    extract_parser.add_argument("image_file", metavar="<PATH>", action='store', default=False, help='the file from which extract the faces.')
    extract_parser.add_argument('--force-recalculation', default=False, action='store_true', help='Force recalculation of operations. Default: False.')

    extract_group_about = extract_parser.add_argument_group('About arguments', 'Showing additional information about this program.')
    extract_group_about.add_argument('-h', '--help', action='help', help='shows this help and exists.')
    extract_group_about.add_argument('--version', action='version', version=f'[%(prog)s] Pyfaces {pyfaces.__version__}', help='shows the version of the program and exits.')

    subparser_alias_generator = subcommands.add_parser(
        "extract",
        help="Extract faces from a file and save encodings",
        parents=[extract_parser]
    )

    guess_parser = argparse.ArgumentParser(
        description='A parser to manage comparisons between faces',
        prog='compare',
        epilog="",
        add_help=False,
        conflict_handler='resolve'
    )

    guess_parser.add_argument('face_path', metavar='<PATH>', action='store', help='The path to the face to be guessed.')
    guess_parser.add_argument('--force-recalculation', default=False, action='store_true', help='Force recalculation of operations. Default: False.')

    guess_group_about = guess_parser.add_argument_group('About arguments', 'Showing additional information about this program.')
    guess_group_about.add_argument('-h', '--help', action='help', help='shows this help and exists.')
    guess_group_about.add_argument('--version', action='version', version=f'[%(prog)s] Pyfaces {pyfaces.__version__}', help='shows the version of the program and exits.')

    subparser_alias_generator = subcommands.add_parser(
        "guess",
        help="Gues which is the most similar candidate to a knowon face",
        parents=[guess_parser]
    )

    # About options
    group_about = parser.add_argument_group('About arguments', 'Showing additional information about this program.')
    group_about.add_argument('-h', '--help', action='help', help='shows this help and exists.')
    group_about.add_argument('--version', action='version', version=f'[%(prog)s] Pyfaces {pyfaces.__version__}', help='shows the version of the program and exits.')

    return parser


def main(params=None):
    """
    Args:
        params: A list with the parameters as grabbed by the terminal. It is
            None when this is called by an entry_point.
    Returns:
        dict: A Json representing the matching results.
    """
    print(text.welcome)

    if params is None:
        parser = get_parser()
        args = parser.parse_args(params)
    else:
        args = params

    # Launch the appropiate util
    if args.command_name:
        try:
            proc = FaceProcessor()
            start_time = time.perf_counter()
            if args.command_name == "compare":
                print(f"[*] Comparing '{emphasis(args.face_path_1)}' with '{emphasis(args.face_path_2)}'…\n")
                result = proc.compare_faces(
                    args.face_path_1, 
                    args.face_path_2, 
                    args.force_recalculation
                )
            elif args.command_name == "extract":
                print(f"[*] Extracting faces from '{emphasis(args.image_file)}'…\n")
                result = proc.extract_faces(
                    args.image_file,
                    args.force_recalculation
                )
            else:
                print(f"[*] Finding closes face to '{emphasis(args.face_path)}'…\n")
                result = proc.guess_face(
                    args.face_path,
                    args.force_recalculation
                )
            print(f"[*] Results: {success(json.dumps(result, indent=2, sort_keys=True))}")
            print()
        except Exception as exc:
            print(f"[*] Results: {error(str(exc))}")
            print()
        elapsed_time = f"{(time.perf_counter() - start_time):.4f}"
        print(f"[*] Execution time: {title(elapsed_time)} seconds")
    else:
        parser.print_help()
    sys.exit(0)

if __name__ == '__main__':
    main()
