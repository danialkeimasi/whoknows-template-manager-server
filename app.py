import api.flask as flaskApp
from config.arg_parse import arg_parse

if __name__ == '__main__':
    flaskApp.app = flaskApp.Flask(__name__)
    flaskApp.feed()

    isThereArg = arg_parse()

    if not isThereArg:
        flaskApp.getApp().run(debug=True, port='3001')

