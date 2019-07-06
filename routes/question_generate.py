from flask import json, request

from flask_restful import reqparse, Api, Resource
from config.config import mongo_client, logger
from modules.template import Template
from config.config import config

from modules.tools import json_tools


questions_sample = json.load(open(config.dir.sample_questions, encoding='utf-8'))


class GenerateQuestionRoute(Resource):
    """
    get question part of api

    api context:
        get the question py post request
    """

    url = '/question/generate'

    def get(self):

        response = {
            'ok': False,
            'error': 'please use post request for get question',
            'request': {
                'tags': ['some tag that you want'],
            }
        }

        return response

    def post(self):

        user_req = request.json
        tags = user_req['tags'] if 'tags' in user_req else None
        count = user_req['count'] if 'count' in user_req else 1

        if tags is None:
            response = {
                "ok": False
            }
        else:

            templates = list(mongo_client.TemplateManager.templates.aggregate([
                {'$match': {'__state': 'in_use'}},
                {'$match': {'tags': {'$in': tags}}},
                {'$sample': {'size': count}},
            ]))
            logger.debug(f'after query for template, number of templates that we found: {len(templates)}')

            questions = []
            for i in range(count):
                for try_count in range(5):
                    try:
                        questions.append(Template(templates[i % len(templates)]).generate_question().dict())
                        break
                    except Exception as e:
                        logger.critical(f'failed in generate question => {type(e)}:{e}')
                else:
                    questions.append(questions_sample[i % len(questions_sample)])

            response = {
                'ok': True,
                'questions': questions,
            }

        return json_tools.to_extended(response)

def add(app):
    Api(app).add_resource(GenerateQuestionRoute, GenerateQuestionRoute.url)
