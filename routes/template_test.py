import flask_restplus
from bson import json_util
from flask import json, request

from config.config import mongo_client
from modules.template import Template
from flask_restful import reqparse, Api, Resource

from modules.tools import json_tools


def add(api):
    @api.route('/template/test_save')
    class TemplateTestRoute(flask_restplus.Resource):
        """
        test the template and update the state
        find template by _id that exist in template
        update the template in the database
        """

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

            return json_tools.to_extended(response)
