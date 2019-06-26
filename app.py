import importlib
import glob
import os

from config.arg_parse import arg_parse
from flask import Flask
from flask_cors import CORS

if __name__ == '__main__':
    app = Flask(__name__)
    CORS(app)
    files = [os.path.basename(path)[:-3] for path in glob.glob('./routes/*.py')
                                            if not os.path.basename(path).startswith('__')]

    for file in files:
        print(file)
        importlib.import_module(f'routes.{file}').add(app)

    isThereArg = arg_parse()

    if not isThereArg:
        app.run(debug=True, host='0.0.0.0', port='3001')
