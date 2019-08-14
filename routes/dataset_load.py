import flask_restplus

from flask import json, request

from config.config import mongo_client

from modules.tools import json_tools

parser = flask_restplus.reqparse.RequestParser()
parser.add_argument(
    'dataset_name',
    type=str,
    help='you must send the "idea" of template as a post json request.',
    required=True
)


def add(api):
    @api.route('/dataset/load')
    class TemplateFindRoute(flask_restplus.Resource):
        """
        find template by query from mongo

        api context:
            find template py post request
        """

        def post(self):

            args = parser.parse_args()
            dataset_name = args['dataset_name']

            dataset = list(mongo_client.data[dataset_name].find())
            if dataset != []:
                json.dump(
                    json_tools.to_extended(dataset),
                    open(f'../datasets/{dataset_name}db.json', mode='w+', encoding='utf-8'),
                    indent=4, ensure_ascii=False
                )

                return {
                    'ok': True,
                    'dataset_size': len(dataset)
                }
            else:
                return {
                    'ok': False,
                    'problem': 'dataset is empty'
                }
