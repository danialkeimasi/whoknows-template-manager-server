import flask_restplus

from config import mongo_client

from modules.tools import json_tools

parser = flask_restplus.reqparse.RequestParser()
parser.add_argument(
    'tags',
    type=list,
    location='json',
    help='you must send the "tags" of template as a post json request.',
    required=False,
    default=None
)
parser.add_argument(
    'count',
    type=int,
    help='you must send the "count" of template as a post json request.',
    required=False,
    default=None
)
parser.add_argument(
    'query',
    type=dict,
    help='you must send the "metadata" of template as a post json request.',
    required=False,
    default=None
)


def add(api):
    @api.route('/template/find')
    class TemplateFindRoute(flask_restplus.Resource):
        """
        find template by query from mongo

        api context:
            find template py post request
        """

        def post(self):
            args = parser.parse_args()

            tags = args['tags']
            count = args['count']
            query = args['query']

            pipeline = []
            pipeline += [{'$match': {'tags': {'$in': tags}}}] if tags is not None else []
            pipeline += [{'$limit': count}] if count is not None else []
            pipeline += [{'$match': query}] if query is not None else []

            templates = list(mongo_client.template_manager.templates.aggregate(pipeline))

            response = {
                'ok': True,
                'templates': templates,
            }

            return json_tools.to_extended(response)
