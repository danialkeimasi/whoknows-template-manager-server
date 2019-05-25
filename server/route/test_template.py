from flask import json, request

from modules.template import Template
from server.flask import getApp


def add():
    app = getApp()

    @app.route('/test_template', methods=['GET'])
    def test_template_get():
        response = {
            'ok': False,
            'error': 'please use post request for testing the ',
            'request': {
                'inside': 'you must send the template as a post request',
            }
        }

        return json.dumps(response)

    @app.route('/test_template', methods=['POST'])
    def test_template_post():
        template = request.json
        run_response = Template(template).test_function()

        return json.dumps(run_response)
