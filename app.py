from importlib import import_module
from os.path import basename
from glob import glob

from bson import json_util
from flask import Flask
from flask_cors import CORS
from flask_restplus import Api

from config.arg_parse import arg_parse


if __name__ == '__main__':

    app = Flask(__name__)
    api = Api(app)

    CORS(app)

    for file in [basename(path).split('.')[0] for path in glob('./routes/*.py') if not basename(path).startswith('__')]:
        import_module(f'routes.{file}').add(api)

    isThereArg = arg_parse()

    if not isThereArg:
        app.run(debug=True, port='3001')
