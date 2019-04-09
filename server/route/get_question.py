from server.flask import getApp
from flask import json, request

from modules.TemplateEngine import create_question

def add():
    app = getApp()
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

