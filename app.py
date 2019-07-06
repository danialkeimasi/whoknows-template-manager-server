from importlib import import_module
from os.path import basename
from glob import glob

from config.arg_parse import arg_parse
from flask_cors import CORS
from bson import json_util
from flask import Flask

class MyConfig(object):
    RESTFUL_JSON = {} # add whatever settings here

    @staticmethod
    def init_app(app):
        app.config['RESTFUL_JSON']['cls'] = app.json_encoder = json_util.default


if __name__ == '__main__':

    app = Flask(__name__)
    app.config.from_object(MyConfig)
    MyConfig.init_app(app)
    CORS(app)

    for file in [basename(path).split('.')[0] for path in glob('./routes/*.py') if not basename(path).startswith('__')]:
        import_module(f'routes.{file}').add(app)

    isThereArg = arg_parse()

    if not isThereArg:
        app.run(debug=True, host='0.0.0.0', port='3001')
