from flask import json

from api.flask import getApp


def add():
    app = getApp()

    @app.route('/', methods=['GET'])
    def index():
        """
        index of api

        page context:
            show the index of question api and links that can go with
        """
        Response = {
            'ok': 1,
            'message': 'question api is on',
            'urls': ['get_question',
                     'check_answer', ]
        }

        return json.dumps(Response)
