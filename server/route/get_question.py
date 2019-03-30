from server.flask import app
from flask import json, request


@app.route('/get_question', methods=['POST', 'GET'])
def get_question():
    '''
    get question part of server

    page context:
        get the question py post request
    '''
    
    Response = ''
    
    if request.method == 'POST':
        Request = request.json


        Response = Request
    
    elif request.method == 'GET':
        Response = {
            'ok': 0,
            'error': 'please use post request for get question',
            'request': {
                'tag': 'some tag that you want',
            }
        }
    
    return json.dumps(Response)