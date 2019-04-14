import server.flask
from flask import Flask

import server.routeHandle as routeHandler
from modules.Tools.ArgParse import arg_parse

server.flask.app = Flask(__name__)
routeHandler.addRoutes()

if __name__ == '__main__':
    isThereArg = arg_parse()

    if not isThereArg:
        server.flask.getApp().run(debug=True, host='0.0.0.0', port='3001')
        # server.flask.getApp().run(debug=True)
