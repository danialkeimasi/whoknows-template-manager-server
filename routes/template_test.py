from bson import json_util
from flask import json, request

from config.config import mongo_client
from modules.template import Template
from flask_restful import reqparse, Api, Resource


class TemplateTest(Resource):
    """
    test the template and update the state
    find template by _id that exist in template
    update the template in the database
    """

    def get(self):

        response = {
            'ok': False,
            'error': 'please use post request for edit the template',
            'request': {
                'template': 'the new verson of template that contain "_id" in it',
            }
        }

        return response

    def post(self):

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


url = '/template/test_save'
def add(app):
    Api(app).add_resource(TemplateTest, url)
