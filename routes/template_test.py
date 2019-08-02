import flask_restplus
from bson import json_util
from flask import json, request

from config.config import mongo_client
from modules.template import Template
from flask_restful import reqparse, Api, Resource

from modules.tools import json_tools
from pprint import pprint


parser = flask_restplus.reqparse.RequestParser()

parser.add_argument(
    'template',
    type=dict,
    help='you must send the template as a json post',
    required=True,
    default={}
)


def add(api):
    @api.route('/template/test_save')
    class TemplateTestRoute(flask_restplus.Resource):
        """
        test the template and update the state
        find template by _id that exist in template
        update the template in the database
        """

        def post(self):

            args = parser.parse_args()
            template = json_tools.to_shell_mode(args['template'])

            updated_template = Template(template).test_update().dict()

            query = {'_id': template['_id']} if '_id' in template else {}

            if query == {}:
                update_response = mongo_client.template_manager.templates.insert_one(updated_template)
                _id = update_response.inserted_id
            else:
                update_response = mongo_client.template_manager.templates.replace_one(query, updated_template, upsert=True)
                _id = template['_id']

            template_updated = mongo_client.template_manager.templates.find_one({'_id': _id})
            response = {
                'ok': update_response.acknowledged,
                '_id': _id,
                'template': template_updated
            }

            return json_tools.to_extended(response)
