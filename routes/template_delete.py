import flask_restplus

from config import mongo_client, logger
from modules.tools import json_tools

parser = flask_restplus.reqparse.RequestParser()
parser.add_argument(
    'query',
    type=dict,
    help='you must send the "metadata" of template as a post json request.',
    required=False,
    default=None
)


def add(api):
    @api.route('/template/delete')
    class TemplateDeleteRoute(flask_restplus.Resource):
        """
        delete template by query from mongo

        api context:
            delete template py post request
        """

        def post(self):
            args = parser.parse_args()
            query = json_tools.to_shell_mode(args['query'])

            mongo_response = mongo_client.template_manager.templates.remove(query)
            response = {
                'ok': bool(mongo_response['n'] != 0),
                'n': mongo_response['n']
            }

            logger.critical(f'query: {query} -> response: {response}')
            return json_tools.to_extended(response)
