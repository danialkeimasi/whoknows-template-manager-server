from server.flask import app
from flask import json, request


@app.route('/', methods=['GET'])
def index():

    '''
    index of server

    page context:
        show the index of question server and links that can go with
    '''
    Response = {
        'ok': 1,
        'message': 'question server is on',
        'urls': 'some',
    }

    return json.dumps(Response)