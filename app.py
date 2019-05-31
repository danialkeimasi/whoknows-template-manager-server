from flask import Flask

from flask_cors import CORS
import server.routesHandler
import server.flask

from config.arg_parse import arg_parse

server.flask.app = Flask(__name__)
CORS(server.flask.getApp())
server.routesHandler.add_routes()

if __name__ == '__main__':
    isThereArg = arg_parse()

    if not isThereArg:
        server.flask.getApp().run(debug=True, host='0.0.0.0', port='30010')
        # server.flask.getApp().run(debug=True)
