from server.flask import app
from flask import json, request


@app.route('/check_answer', methods=['POST', 'GET'])
def check_answer():
    '''
    check the answer of a question

    page context:
        check the answer of question by a post request
    '''
    
    Response = ''

    if request.method == 'POST':
        Request = request.json


        Response = Request
    
    elif request.method == 'GET':
        Response = {
            'ok': 0,
            'error': 'please use post request for check Ans',
            'request': {
                'id': 'question ID',
                'answer': 'answer or answers',
            }
        }
    
    return json.dumps(Response)
