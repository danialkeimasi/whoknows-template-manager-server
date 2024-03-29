import traceback

import flask_restplus
from flask import json

from config import mongo_client, logger, SETTINGS
from modules.template import Template
from modules.tools import json_tools
from modules.tools.functions import traceback_shortener

questions_sample = json.load(open(SETTINGS.dir.sample_questions, encoding='utf-8'))

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
    'query',
    type=dict,
    help='you must send the "metadata" of template as a post json request.',
    required=False,
    default=None
)
parser.add_argument(
    'count',
    type=int,
    help='you must send the "count" of template as a post json request.',
    required=True
)
parser.add_argument(
    'metadata',
    type=dict,
    help='you must send the "metadata" of template as a post json request.',
    required=False,
    default={}
)


def add(api):
    @api.route('/question/generate')
    class GenerateQuestionRoute(flask_restplus.Resource):
        """
        get question part of api

        api context:
            get the question py post request
        """

        def post(self):

            args = parser.parse_args()

            tags = args['tags']
            query = args['query']
            count = args['count']
            metadata = args['metadata']

            pipeline = [{'$match': {'__state': 'in_use'}}]
            pipeline += [{'$match': {'tags': {'$in': tags}}}] if tags is not None else []
            pipeline += [{'$sample': {'size': max(3, count)}}] if count is not None else []
            pipeline += [{'$match': query}] if query is not None else []

            templates = list(mongo_client.template_manager.templates.aggregate(pipeline))

            logger.critical(f'pipeline for aggregation: {pipeline} -> we found {len(templates)}.')

            if templates == []:
                return json_tools.to_extended({
                    'ok': False,
                    'problem': 'there is no template match.',
                })

            questions = []
            try_count = 5
            i = 0
            while (len(questions) < count) and (i < count * try_count):
                for _ in range(try_count):
                    try:
                        questions.append(Template(templates[i % len(templates)]).generate_question(
                            metadata=metadata).raise_if_problems().dict())

                    except Exception as e:
                        error_message = traceback_shortener(traceback.format_exc())
                        logger.error(f'failed in generate question => {error_message}')

                    else:
                        break

                else:
                    # TODO: do some report for this template to the database
                    pass

                i += 1

            logger.critical(f'after genere questions -> ok={len(questions) == count} and we make {len(questions)} questions.')

            return json_tools.to_extended({
                'ok': len(questions) == count,
                'questions': questions,
            })
