from server.flask import getApp
from flask import json, request
from config.config import config, mongo_client
import random
import functools
import glob
from modules.template import Template


def add():
    app = getApp()
    @app.route('/get_question', methods=['GET'])
    def get_question_get():

        response = {
            'ok': False,
            'error': 'please use post request for get question',
            'request': {
                'tags': ['some tag that you want'],
            }
        }

        return json.dumps(response)

    @app.route('/get_question', methods=['POST'])
    def get_question_post():
        '''
        get question part of server

        api context:
            get the question py post request
        '''
        user_req = request.json
        tags     = user_req['tags']     if 'tags' in user_req else None
        count    = user_req['count']    if 'count' in user_req else 1

        if tags is None or count is None:
            response = {
                "ok": False
            }
        else:
            # 1 find the templates that $match with tags that we want and use $sample
            #   for select number of templates randomly

            # 2 generate a list of questiostions by len of "count"

            # 3 prepare response dictionary and return it with json.dump

            templates = list(mongo_client.TemplateManager.templates.aggregate([
                            {'$match' : {'tags': { '$in' : tags } } },
                            {'$sample': {'size': count} },
                            ]))

            response = {
                'ok': True,
                'questions': (questions * 100)[:count]#[Template(template).generate_question().dict() for template in templates],
            }

        return json.dumps(response)



questions = [
    {
        'type'          : 'bool',
        'title'         : {
            'text'      : ['This title section of a sample bool question']
        },
        'subtitle'      : {
            'text'      : ['This subtitle section of a sample bool question']
        },
        'choice'        : {
            'text'      : ['This choice section of a sample bool question']
        },
        'answer'        : {
            'text'      : ['true']
        }
    },
    {
        'type'          : 'choose',
        'title'         : {
            'text'      : ['This title section of a sample choose question']
        },
        'subtitle'      : {
            'text'      : ['This subtitle section of a sample choose question']
        },
        'choice'        : {
            'text'      : ['choice number 1', 'choice number 2', 'choice number 3', 'choice number 4']
        },
        'answer'        : {
            'text'      : ['choice number 1']
        }
    },
    {
        'type'          : 'select',
        'title'         : {
            'text'      : ['This title section of a sample select question']
        },
        'subtitle'      : {
            'text'      : ['This subtitle section of a sample select question']
        },
        'choice'        : {
            'text'      : ['choice number 1', 'choice number 2', 'choice number 3', 'choice number 4']
        },
        'answer'        : {
            'text'      : ['choice number 1', 'choice number 2']
        }
    },
    {
        'type'          : 'write',
        'title'         : {
            'text'      : ['This title section of a sample write question']
        },
        'subtitle'      : {
            'text'      : ['This subtitle section of a sample select question']
        },
        'answer'        : {
            'text'      : ['answer']
        }
    }
]