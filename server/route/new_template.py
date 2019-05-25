from server.flask import getApp
from flask import json, request
from config.config import config, mongo_client, logger
from modules.template import Template


def add():
    app = getApp()
    @app.route('/template/new', methods=['GET'])
    def new_template_get():

        response = {
            'ok': False,
            'error': 'please use post request to add new template to server',
            'request': {
                'idea': 'the idea of template',
            }
        }

        return json.dumps(response)

    @app.route('/template/new', methods=['POST'])
    def new_template_post():
        '''
        find template by query from mongo

        api context:
            find template py post request
        '''
        user_req = request.json     if request.json is not None else {}
        idea     = user_req['idea'] if 'idea' in user_req else None

        if idea:
            empty_template = json.load(open())
            response = {
                'ok': True,
                'templates': templates,
            }

        
        return json.dumps(response)
