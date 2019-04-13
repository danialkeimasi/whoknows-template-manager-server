from server.flask import getApp
from flask import json, request
from modules.Config import CONFIG

from modules.TemplateEngine import testTemplate_ByCreate_Question

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
        # question = create_question(Request['tags'], Request['count'])
        
        Request = request.json
        rand = Request['rand']

        questions = testTemplate_ByCreate_Question(open(f'{CONFIG.templates_dir}/../moein_f/football_{rand}.json'))

        return json.dumps(questions)