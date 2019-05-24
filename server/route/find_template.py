from server.flask import getApp
from flask import json, request
from config.config import config, mongo_client, logger
import random
import functools
import glob
from modules.template import Template


def add():
    app = getApp()
    @app.route('/find_template', methods=['GET'])
    def find_template_get():

        response = {
            'ok': False,
            'error': 'please use post request for find template',
            'request': {
                'tags': ['some tag that you want'],
            }
        }

        return json.dumps(response)

    @app.route('/get_question', methods=['POST'])
    def find_template_post():
        '''
        find template by query from mongo

        api context:
            find template py post request
        '''
        user_req = request.json
        tags     = user_req['tags']     if 'tags'  in user_req else None
        count    = user_req['count']    if 'count' in user_req else 10
        ok       = user_req['ok']       if 'ok'    in user_req else True
    
        templates = list(mongo_client.TemplateManager.templates.aggregate([
                        {'$match' : {'ok': ok} },
                        {'$match' : {'tags': { '$in' : tags } } },
                        {'$sample': {'size': count} },
                        ]))

        response = {
            'ok': True,
            'questions': templates,
        }

        return json.dumps(response)
