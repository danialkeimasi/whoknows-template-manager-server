from importlib import import_module
from os.path import basename
from glob import glob

from flask import json
from flask_restful import Api, Resource

class ApiIndexRoute(Resource):
    """
        index of api

        page context:
            show the index of question api and links that can go with
    """

    url = '/'

    def get(self):

        Response = {
            'ok': True,
            'message': 'question api is on',
            'routes': {
                Route.url: Route.__doc__.strip() for Route in Resource.__subclasses__()
            }
        }

        return Response


def add(app):
    Api(app).add_resource(ApiIndexRoute, ApiIndexRoute.url)
