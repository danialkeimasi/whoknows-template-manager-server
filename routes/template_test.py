import flask_restplus
from bson import json_util
from flask import json, request

from config.config import mongo_client
from modules.template import Template
from flask_restful import reqparse, Api, Resource

from modules.tools import json_tools
from pprint import pprint


def add(api):
    @api.route('/template/test_save')
    class TemplateTestRoute(flask_restplus.Resource):
        """
        test the template and update the state
        find template by _id that exist in template
        update the template in the database
        """

        def post(self):

            user_req = json_util.loads(request.data) if json_util.loads(request.data) is not None else {}
            template = user_req['template'] if 'template' in user_req else {}

            problems = []
            problems += ['you must send the template as a json post'] if template == {} else []

            if problems == []:

                updated_template = Template(template).test_update().dict()

                query = {'_id': template['_id']} if '_id' in template else {}

                if query == {}:
                    update_response = mongo_client.template_manager.templates.insert_one(updated_template)
                else:
                    update_response = mongo_client.template_manager.templates.replace_one(query, updated_template, upsert=True)

                pprint(update_response)

                template_updated = mongo_client.template_manager.templates.find_one({'_id': template['_id']})
                response = {
                    'ok': update_response['ok'],
                    '_id': template['_id'],
                    'template': template_updated
                }

            else:
                response = {
                    'ok': False,
                    'problem': problems,
                }

            return json_tools.to_extended(response)
