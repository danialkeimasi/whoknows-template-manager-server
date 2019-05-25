from flask import json, request

from config.config import mongo_client, logger
from modules.template import Template
from server.flask import getApp


def add():
    app = getApp()
    @app.route('/question/generate', methods=['GET'])
    def get_question_get():

        response = {
            'ok': False,
            'error': 'please use post request for get question',
            'request': {
                'tags': ['some tag that you want'],
            }
        }

        return json.dumps(response)

    @app.route('/question/generate', methods=['POST'])
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
            
            templates = list(mongo_client.TemplateManager.templates.aggregate([
                            {'$match' : {'ok': True} },
                            {'$match' : {'tags': { '$in' : tags } } },
                            {'$sample': {'size': count} },
                            ]))

            questions = []
            
            for i in range(count):
                for try_count in range(5):
                    try:
                        questions.append(Template(templates[i % len(templates)]).generate_question().dict())
                        break
                    except Exception as e:
                        logger.critical(f'faild in generate question :{e}')
                else:
                    questions.append(questions_sample[i % len(questions_sample)])
                

            response = {
                'ok': True,
                'questions': questions,
            }

        return json.dumps(response)



questions_sample = [
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