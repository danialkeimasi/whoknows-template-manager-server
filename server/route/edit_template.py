from server.flask import getApp
from flask import json, request
from config.config import config, mongo_client, logger
from modules.template import Template
from bson import json_util, ObjectId


def add():
    app = getApp()
    @app.route('/template/edit', methods=['GET'])
    def edit_template_get():

        response = {
            'ok': False,
            'error': 'please use post request for edit the template',
            'request': {
                'template': 'the new verson of template that contain "_id" in it',
            }
        }

        return json.dumps(response)

    @app.route('/template/edit', methods=['POST'])
    def edit_template_post():
        '''
        find template by _id that exist in template
        update the template in the database
        
        '''
        user_req = request.json if request.json is not None else {}
        template = json_util.loads(user_req)

        problems = []
        problems += ['you must send the template as a json post']                    if template is {} else []
        problems += ['the template must have "_id" property that exists in mongodb'] if '_id' not in template else []

        if problems == []:
            replace_res = mongo_client.TemplateManager.templates.replace_one({'_id': template['_id']}, template)
            response = {
                'ok' : replace_res.acknowledged,
                '_id': replace_res.upserted_id,
            }
        else:
            response = {
                'ok': False,
                'problem': problems,
            }

        return json_util.dumps(response)
