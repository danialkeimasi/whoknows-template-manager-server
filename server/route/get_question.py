from server.flask import app
from flask import json, request
import requests

from pprint import pprint
from modules.TemplateEngine import create_question

@app.route('/get_question', methods=['GET'])
def get_question_get():
    
    Response = {
        'ok': False,
        'error': 'please use post request for get question',
        'request': {
            'tags': ['some tag that you want'],
        }
    }
    
    return json.dumps(Response)

@app.route('/get_question', methods=['POST'])
def get_question_post():
    '''
    get question part of server

    page context:
        get the question py post request
    '''
    Request = request.json
    question = create_question(Request['tags'], Request['count'])
    
    return json.dumps(question)

