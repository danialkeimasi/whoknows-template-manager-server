import importlib
import glob
import os

from flask_restful import Resource, Api
from flask_cors import CORS
from flask import Flask


def getApp():
    return app

def getApi():
    return api_app


def add_routes():
    """ add the routes to the flask app. """

    files = [os.path.basename(path)[:-3] for path in glob.glob('./api/routes/*.py')
                                            if not os.path.basename(path).startswith('__')]

    for file in files:
        importlib.import_module(f'api.routes.{file}').add()


def feed():
    CORS(app)
    api_app = Api(app)


    add_routes()




if __name__ == "__main__":
    app = None
    api_app = None