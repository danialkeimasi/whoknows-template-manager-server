from server.flask import getApp
from flask import json, request
from modules.Config import CONFIG
import random
import functools
import glob

from modules.TemplateEngine import testTemplate_ByCreate_Question

def add():
    app = getApp()
    @app.route('/get_question', methods=['GET'])
    def get_question_get():

        response = {
            'ok': False,
            'error': 'please use post request for get question',
            'request': {
                'tags': ['some tag that you want'],
            }
        }

        return json.dumps(response)

    @app.route('/get_question', methods=['POST'])
    def get_question_post():
        '''
        get question part of server

        page context:
            get the question py post request
        '''
        user_req = request.json
        tags     = user_req['tags']     if 'tags' in user_req else None
        metadata = user_req['metadata'] if 'metadata' in user_req else {}
        count    = user_req['count']    if 'count' in user_req else 1
        

        # 1 find the templates that $match with tags that we want and use $sample
        #   for select number of templates randomly

        # 2 generate a list of questiostions by len of "count"

        # 3 prepare response dictionary and return it with json.dump
        
        templates = 'mongo query'
        questions = 'list of generated questions with templates'

        response = {
            'ok': True,
            'questions': questions,
        }

        return json.dumps(response)
