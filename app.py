from importlib import import_module
from glob import glob
from os.path import basename

from config.arg_parse import arg_parse
from flask import Flask
from flask_cors import CORS

if __name__ == '__main__':
    app = Flask(__name__)
    CORS(app)

    for file in [basename(path).replace('.py', '') for path in glob('./routes/*.py') if not basename(path).startswith('__')]:
        import_module(f'routes.{file}').add(app)

    isThereArg = arg_parse()

    if not isThereArg:
        app.run(debug=True, host='0.0.0.0', port='3001')

