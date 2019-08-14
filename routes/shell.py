import io
import subprocess

import flask_restplus

from modules.tools import json_tools

parser = flask_restplus.reqparse.RequestParser()
parser.add_argument(
    'command',
    type=str,
    help='you must send the "command" as a post json request.',
    required=True
)


def add(api):
    @api.route('/shell')
    class ShellRoute(flask_restplus.Resource):
        """
        """

        def post(self):
            args = parser.parse_args()
            command = args['command'].split()

            proc = subprocess.Popen(["python3", "app.py"] + command, stdout=subprocess.PIPE)
            response_list = [line for line in io.TextIOWrapper(proc.stdout, encoding="utf-8")]

            return json_tools.to_extended({
                'response': response_list
            })
