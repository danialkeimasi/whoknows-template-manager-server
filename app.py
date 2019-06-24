import api.flask as flaskApp

from flask import Flask
from flask_cors import CORS
from config.arg_parse import arg_parse

if __name__ == '__main__':
    flaskApp.app = Flask(__name__)
    CORS(flaskApp.getApp())
    flaskApp.add_routes()

    isThereArg = arg_parse()

    if not isThereArg:
        flaskApp.getApp().run(debug=True, host='0.0.0.0', port='3001')
