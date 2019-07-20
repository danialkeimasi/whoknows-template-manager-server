import flask_restplus
import json
import traceback
from flask import json, request

from config.config import mongo_client, logger, config
from modules.template import Template
from modules.tools import json_tools
from modules.tools.functions import traceback_shortener

questions_sample = json.load(open(config.dir.sample_questions, encoding='utf-8'))



parser = flask_restplus.reqparse.RequestParser()
parser.add_argument(
    'tags',
    type=list,
    help='you must send the "idea" of template as a post json request.',
    required=True
)
parser.add_argument(
    'count',
    type=int,
    help='you must send the "idea" of template as a post json request.',
    required=True
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

            user_req = request.json
            tags = user_req['tags'] if 'tags' in user_req else None
            count = user_req['count'] if 'count' in user_req else 1

            if tags is None:
                response = {
                    "ok": False
                }
            else:

                templates = list(mongo_client.template_manager.templates.aggregate([
                    {'$match': {'__state': 'in_use'}},
                    {'$match': {'tags': {'$in': tags}}},
                    {'$sample': {'size': count}},
                ]))
                logger.debug(f'after query for template, number of templates that we found: {len(templates)}')

                questions = []

                try_count = 5
                i = 0
                while (len(questions) < count) and (i < count * try_count):
                    for _ in range(try_count):
                        try:
                            questions.append(Template(templates[i % len(templates)]).generate_question().raise_if_problems().dict())
                            break
                        except Exception as e:
                            error_message = traceback_shortener(traceback.format_exc())
                            logger.error(f'failed in generate question => {error_message}')
                    else:
                        # TODO: do some report for this template to the database
                        pass

                    i += 1

                response = {
                    'ok': len(questions) == count,
                    'questions': questions,
                }

            return json_tools.to_extended(response)
