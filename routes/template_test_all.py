import flask_restplus
from bson import json_util
from flask import json, request

from config.config import mongo_client
from modules.template import Template
from flask_restful import reqparse, Api, Resource

from modules.tools import json_tools


def add(api):
    @api.route('/template/test_all')
    class TemplateTestRoute(flask_restplus.Resource):
        """
        test the template and update the state
        find template by _id that exist in template
        update the template in the database
        """

        def post(self):

            templates = list(mongo_client.template_manager.templates.find())
            results = []
            for template in templates:

                updated_template = Template(template).test_update().dict()
                replace_response = mongo_client.template_manager.templates.replace_one({'_id': template['_id']}, updated_template)
                results.append(replace_response.acknowledged)

            response = {
                'ok': all(results),
                'problem': [],
                'result':{
                    'template_count': len(templates)
                }
            }

            return json_tools.to_extended(response)
