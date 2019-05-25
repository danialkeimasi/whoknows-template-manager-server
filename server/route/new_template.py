from server.flask import getApp
from flask import json, request
from config.config import config, mongo_client, logger
from modules.template import Template
from modules.tools.json_mongo_encoder import JSONEncoder
from bson import json_util, ObjectId


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
            empty_template = json.load(open(config.dir.empty_template))
            empty_template['__idea'] = idea
            insert_object = mongo_client.TemplateManager.templates.insert_one(empty_template)
            response = {
                'ok' : insert_object.acknowledged,
                '_id': insert_object.inserted_id
            }
        else:
            response = {
                'ok' : False,
                'problem': ['you must send the idea as a post json request.'],
            }
        
        return json_util.dumps(response)
