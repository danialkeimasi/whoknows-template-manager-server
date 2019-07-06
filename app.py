from importlib import import_module
from os.path import basename
from glob import glob

from config.arg_parse import arg_parse
from flask_cors import CORS
from bson import json_util
from flask import Flask

class MyConfig(object):
    RESTFUL_JSON = {'cls': json_util.object_pairs_hook}

if __name__ == '__main__':

    app = Flask(__name__)
    # app.config.from_object(MyConfig)
    CORS(app)

    for file in [basename(path).split('.')[0] for path in glob('./routes/*.py') if not basename(path).startswith('__')]:
        import_module(f'routes.{file}').add(app)

    isThereArg = arg_parse()

    if not isThereArg:
        app.run(debug=True, port='3001')
