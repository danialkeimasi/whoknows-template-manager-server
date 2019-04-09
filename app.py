from modules.Tools.ArgParse import arg_parse

import server.flask
from flask import Flask

server.flask.app = Flask(__name__)
import server.routeHandle


if __name__ == '__main__':
    if not arg_parse():
        # server.flask.app.run(debug=True, host='0.0.0.0', port='3001')
        server.flask.app.run(debug=True)
