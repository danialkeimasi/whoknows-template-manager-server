from bson import json_util
from flask import json, request

from config.config import mongo_client
from api.flask import getApp
from modules.template import Template


def add():
    app = getApp()

    @app.route('/template/test_save', methods=['GET'])
    def edit_template_get():

        response = {
            'ok': False,
            'error': 'please use post request for edit the template',
            'request': {
                'template': 'the new verson of template that contain "_id" in it',
            }
        }

        return json.dumps(response)

    @app.route('/template/test_save', methods=['POST'])
    def edit_template_post():
        """
        test the template and update the state
        find template by _id that exist in template
        update the template in the database
        
        """
        user_req = json_util.loads(request.data) if request.json is not None else {}
        template = user_req['template'] if 'template' in user_req else {}

        problems = []
        problems += ['you must send the template as a json post'] if template == {} else []
        problems += ['the template must have "_id" property that exists in mongodb'] if '_id' not in template else []

        if problems == []:
            
            updated_template = Template(template).test_update().dict()
            replace_response = mongo_client.TemplateManager.templates.replace_one({'_id': template['_id']}, updated_template)

            template_updated = mongo_client.TemplateManager.templates.find_one({'_id': template['_id']})
            response = {
                'ok': replace_response.acknowledged,
                '_id': template['_id'],
                'template': template_updated
            }

        else:
            response = {
                'ok': False,
                'problem': problems,
            }

        return json_util.dumps(response)
