from bson import json_util
from flask import json, request

from config.config import mongo_client
from server.flask import getApp


def add():
    app = getApp()

    @app.route('/template/find', methods=['GET'])
    def find_template_get():
        response = {
            'ok': False,
            'error': 'please use post request for find template',
            'request': {
                'tags': ['some tag that you want'],
            }
        }

        return json.dumps(response)

    @app.route('/template/find', methods=['POST'])
    def find_template_post():
        '''
        find template by query from mongo

        api context:
            find template py post request
        '''
        user_req = json_util.loads(request.data) if request.json is not None else {}
        query = user_req['query'] if 'query' in user_req else None
        tags = user_req['tags'] if 'tags' in user_req else None
        ok = user_req['ok'] if 'ok' in user_req else None
        count = user_req['count'] if 'count' in user_req else None

        pipeline = []
        pipeline += [{'$match': query}] if query is not None else []
        pipeline += [{'$match': {'ok': ok}}] if ok is not None else []
        pipeline += [{'$match': {'tags': {'$in': tags}}}] if tags is not None else []
        pipeline += [{'$limit': count}] if count is not None else []

        templates = list(mongo_client.TemplateManager.templates.aggregate(pipeline))

        response = {
            'ok': True,
            'templates': templates,
        }

        return json_util.dumps(response)