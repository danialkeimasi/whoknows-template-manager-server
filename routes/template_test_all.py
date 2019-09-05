import flask_restplus

from config import mongo_client
from modules.template import Template
from modules.tools import json_tools


def add(api):
    @api.route('/template/test_all')
    class TemplateTestAllRoute(flask_restplus.Resource):
        """
        test the templates and update the state of all templates
        """

        def post(self):
            templates = list(mongo_client.template_manager.templates.find())
            results = []
            for template in templates:
                updated_template = Template(template).test_update().dict()
                replace_response = mongo_client.template_manager.templates.replace_one({'_id': template['_id']},
                                                                                       updated_template)
                results.append(replace_response.acknowledged)

            response = {
                'ok': all(results),
                'problem': [],
                'result': {
                    'template_count': len(templates)
                }
            }

            return json_tools.to_extended(response)
