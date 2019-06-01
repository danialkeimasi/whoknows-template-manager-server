from flask import Flask

from flask_cors import CORS
import api.routesHandler
import api.flask

from config.arg_parse import arg_parse

api.flask.app = Flask(__name__)
CORS(api.flask.getApp())
api.routesHandler.add_routes()

if __name__ == '__main__':
    isThereArg = arg_parse()

    if not isThereArg:
        api.flask.getApp().run(debug=True, host='0.0.0.0', port='3001')
        # api.flask.getApp().run(debug=True)

# from modules.template import Template
# from pprint import pprint

# t = Template('d:/Programming/Python/whoKnows/guessit-question-manager/templates/moein_f/football_team1.json', mode='file')
# t.test_update()
# # pprint(t.dict())
