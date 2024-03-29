import flask_restplus

from config import mongo_client, logger
from modules.tools import json_tools

parser = flask_restplus.reqparse.RequestParser()
parser.add_argument(
    'count',
    type=int,
    help='number of questions',
    required=False,
    default=None
)
parser.add_argument(
    'query',
    type=dict,
    help='mongo query',
    required=False,
    default=None
)


def add(api):
    @api.route('/question/find')
    class QuestionFindRoute(flask_restplus.Resource):
        """
        find question by query from mongo

        api context:
            find question py post request
        """

        def post(self):
            args = parser.parse_args()

            count = args['count']
            query = args['query']

            pipeline = []
            pipeline += [{'$match': query}] if query is not None else []
            pipeline += [{'$limit': count}] if count is not None else []


            questions = list(mongo_client.template_manager.questions.aggregate(pipeline))

            logger.critical(f'question_query: {query}, count: {count} -> we found {len(questions)} question.')

            response = {
                'ok': True,
                'questions': questions,
            }

            return json_tools.to_extended(response)
