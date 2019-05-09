from flask import Flask

import server.flask
import server.routeHandle
from config.arg_parse import arg_parse

server.flask.app = Flask(__name__)
server.routeHandle.addRoutes()

if __name__ == '__main__':
    isThereArg = arg_parse()

    if not isThereArg:
        server.flask.getApp().run(debug=True, port='3001')
        # server.flask.getApp().run(debug=True)

