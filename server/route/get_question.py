from server.flask import getApp
from flask import json, request
from modules.Config import CONFIG
import random
import functools

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
        count = Request['count']
        # tags  = Request['tags']

        questions = []
        for i in range(1, 9):
            try:
                questions += [ testTemplate_ByCreate_Question(json.load(open(f'./templates/moein_f/football_{i}.json'))) ]
            
            except Exception as error:
                pass

        questions =  functools.reduce(lambda a, b: a + b, questions)

        
        for i, item in enumerate(questions):
            if not item['active']:
                questions.pop(i)
        

        if len(questions) < count:
            return json.dumps({ 
                    'ok': False, 
                    'problem': 'not enought questions !'
                })
        
        else:
            return json.dumps({
                'ok': True,
                'questions': questions[:count]
            })
