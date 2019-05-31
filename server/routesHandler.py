import glob
import importlib
import os


def add_routes():
    """ add the routes to the flask app. """

    files = [os.path.basename(path)[:-3] for path in glob.glob('./server/routes/*.py')
                                            if not os.path.basename(path).startswith('__')]

    for file in files:
        importlib.import_module(f'server.routes.{file}').add()