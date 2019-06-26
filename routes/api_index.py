from flask import json
from flask_restful import Api, Resource

class ApiIndex(Resource):
    """
        index of api

        page context:
            show the index of question api and links that can go with
    """

    def get(self):

        Response = {
            'ok': True,
            'message': 'question api is on',
            'urls': ['get_question',
                     'check_answer',
            ]
        }

        return Response


def add(app):
    Api(app).add_resource(ApiIndex, '/')
