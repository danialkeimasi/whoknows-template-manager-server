import api.flask as flaskApp
from config.arg_parse import arg_parse

if __name__ == '__main__':
    flaskApp.app = flaskApp.Flask(__name__)
    flaskApp.feed()

    isThereArg = arg_parse()

    if not isThereArg:
        flaskApp.getApp().run(debug=True, host='0.0.0.0', port='3001')
