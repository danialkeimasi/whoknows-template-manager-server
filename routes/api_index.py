from importlib import import_module
from os.path import basename
from glob import glob

from flask import json
from flask_restful import Api, Resource

routes = []
for file in [basename(path).split('.')[0] for path in glob('./routes/*.py') if not basename(path).startswith('__') and not basename(path).startswith('api_index')]:
        routes.append(import_module(f'routes.{file}').url)

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
            'routes': routes
        }

        return Response


url = '/'
def add(app):
    Api(app).add_resource(ApiIndex, url)
