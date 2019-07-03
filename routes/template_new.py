from bson import json_util
from flask import json, request

from config.config import config, mongo_client
from flask_restful import reqparse, Api, Resource


class TemplateNew(Resource):
    """
    find template by query from mongo

    api context:
        find template py post request
    """

    def get(self):

        response = {
            'ok': False,
            'error': 'please use post request to add new template to api',
            'request': {
                'idea': 'the idea of template',
            }
        }

        return response

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'idea',
            type=str,
            help='you must send the "idea" of template as a post json request.',
            required=True
        )
        args = parser.parse_args()

        idea = args['idea']

        empty_template = json.load(open(config.dir.empty_template))
        empty_template['__idea'] = idea

        insert_object = mongo_client.TemplateManager.templates.insert_one(empty_template)

        template = mongo_client.TemplateManager.templates.find_one({'_id': insert_object.inserted_id})

        response = {
            'ok': insert_object.acknowledged,
            '_id': insert_object.inserted_id,
            'template': template
        }

        return json_util.dumps(response)


def add(app):
    Api(app).add_resource(TemplateNew, '/template/new')
