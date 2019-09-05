import flask_restplus
from flask import json

from config.config import config, mongo_client
from modules.tools import json_tools

parser = flask_restplus.reqparse.RequestParser()
parser.add_argument(
    'name',
    type=str,
    help='you must send the "name" of template as a post json request.',
    required=True
)


def add(api):
    @api.route('/template/new')
    class TemplateNewRoute(flask_restplus.Resource):
        """
        find template by query from mongo

        api context:
            find template py post request
        """

        def post(self):
            args = parser.parse_args()

            name = args['name']

            empty_template = json.load(open(config.dir.empty_template))
            empty_template['__name'] = name

            insert_object = mongo_client.template_manager.templates.insert_one(empty_template)

            template = mongo_client.template_manager.templates.find_one({'_id': insert_object.inserted_id})

            response = {
                'ok': insert_object.acknowledged,
                '_id': insert_object.inserted_id,
                'template': template
            }

            return json_tools.to_extended(response)
