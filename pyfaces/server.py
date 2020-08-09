################################################################################
#
#    Copyright 2020 @ Félix Brezo (@febrezo)
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
from jsonrpc import JSONRPCResponseManager, dispatcher

from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple

import pyfaces
import pyfaces.misc.text as text
from pyfaces.core.processor import FaceProcessor
from pyfaces.core.configuration import ConfigManager


@dispatcher.add_method
def compare_faces(face_path_1, face_path_2):
    """Compare two faces

    Args:
        face_path_1 (str): The path to the image of the first face.
        face_path_1 (str): The path to the image of the second face.

    Return:
        double. The similarity value in a domain [0, 1].
    """
    proc = FaceProcessor()
    return proc.compare(face_path_1, face_path_2)


@dispatcher.add_method
def config():
    """Return configuration"""
    return ConfigManager().get()


@dispatcher.add_method
def set_config(name, value):
    """Set a configuration attribute
    """
    config = ConfigManager()
    config.set(name, value)
    return "Configuration 'name' changed to 'value'."


@dispatcher.add_method
def extract_faces(image_path):
    """Extract faces from an image

    Args:
        image_path (str): The path to the image which will be searched for images.
    """
    proc = FaceProcessor()
    return proc.extract_faces(image_path)


@dispatcher.add_method
def delete_analysis(image_path):
    """The analysis to remove

    Args:
        image_path (str): The path to the source image to delete.
    """
    proc = FaceProcessor()
    return proc.delete_path(image_path)


@dispatcher.add_method
def get_face(face_path):
    """Get the face configuration

    Warning! This could be used to gab other files! Watch out!

    Args:
        face_path (str): The path to the face which is used as a key.
    """
    proc = FaceProcessor()
    return proc.get_face(face_path)


@dispatcher.add_method
def get_image(image_path):
    """Get the base64 image

    Security Warning! This could be used to gab other files! Watch out!

    Args:
        image_path (str): The image path to the file to be grabbed.
    """
    proc = FaceProcessor()
    return proc.get_image(image_path)

@dispatcher.add_method
def get_metadata(image_path):
    """Get the metadata from a source image

    Warning! This could be used to gab other files! Watch out!

    Args:
        image_path (str): The path to the image which is used as a key.
    """
    proc = FaceProcessor()
    return proc.get_metadata(image_path)

@dispatcher.add_method
def guess_face(face_path):
    """Compare a given face with all the known faces
    """
    proc = FaceProcessor()
    return proc.guess_face(face_path)


@dispatcher.add_method
def info():
    """Get server information
    """
    proc = FaceProcessor()
    return {
        "name": f"Pyfaces {pyfaces.__version__} JSON-RPC Server",
        "methods": [
            "compare_faces",
            "config",
            "extract_faces",
            "get_face",
            "get_image",
            "get_metadata",
            "guess_face",
            "info",
            "set_config"
        ],
        "faces": len(proc.encodings)
    }


@Request.application
def application(request):
    response = JSONRPCResponseManager.handle(
        request.data,
        dispatcher
    )
    return Response(response.json, mimetype='application/json')


def get_parser():
    """Defines the argument parser
    Returns:
        argparse.ArgumentParser.
    """
    config = ConfigManager()

    parser = argparse.ArgumentParser(
        description= 'Pyfaces JSON-RPC Server | A face recognition tool to make it accesible for everyone and learn from it to what extent we are exposed.',
        prog='pyfacesd',
        add_help=False,
        conflict_handler='resolve'
    )

    # Selecting the platforms where performing the search
    group_server = parser.add_argument_group('JSON-RPC arguments', 'Configuration folders')
    group_server.add_argument('-h', '--host', metavar='<HOST>', required=False, default="localhost", action='store', help="the host where it will be launched. Note that '0.0.0.0' will make it accesible from outside and this can be dangerous. Default value: localhost.")
    group_server.add_argument('-p', '--port', metavar='<PORT>', required=False, default=12012, action='store', help='select the port in which the JSON RPC server will be deployed. Default value: 12012.')
    group_server.add_argument('-t', '--threads', metavar='<NUM>', required=False, default=config.get_attribute("num_threads"), action='store', help=f"select the number of threads to be used. Default value: {config.get_attribute('num_threads')}")

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

    try:
        run_simple(
            args.host,
            args.port,
            application
        )
    except KeyboardInterrupt:
        print()
        print("Manually stopped by the user.")


if __name__ == '__main__':
    main()
