# from flask import Flask
#
# import server.flask
# import server.routeHandle
# from modules.Tools.ArgParse import arg_parse
#
# server.flask.app = Flask(__name__)
# server.routeHandle.addRoutes()
#
# if __name__ == '__main__':
#     isThereArg = arg_parse()
#
#     if not isThereArg:
#         server.flask.getApp().run(debug=True, host='0.0.0.0', port='3001')
#         # server.flask.getApp().run(debug=True)


from pprint import pprint
import json
from modules.template import Template


if __name__ == '__main__':
    template = Template(json.load(open('templates/template_v2_moein/football_team1.json')))

    if template.problems():
        print('errors', template.problems())
    else:
        pprint(template.generate_question().dict())
