import flask_restplus

from bson import json_util
from flask import json, request

from flask_restful import reqparse, Api, Resource
from config.config import mongo_client

from modules.tools import json_tools

def add(api):
    @api.route('/template/find')
    class TemplateFindRoute(flask_restplus.Resource):
        """
        find template by query from mongo

        api context:
            find template py post request
        """

        def post(self):

            user_req = json_util.loads(request.data) if json_util.loads(request.data) is not None else {}
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

            return json_tools.to_extended(response)