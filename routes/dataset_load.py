import os

import flask_restplus

from flask import json, request

from config.config import mongo_client

from modules.tools import json_tools

parser = flask_restplus.reqparse.RequestParser()
parser.add_argument(
    'dataset_names',
    type=list,
    location='json',
    help='query with names',
    required=False,
    default=[]
)
parser.add_argument(
    'query',
    type=dict,
    help='mongo query',
    required=False,
    default={}
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
            dataset_dir = '../datasets/'

            args = parser.parse_args()
            dataset_query = args['query']
            dataset_names = args['dataset_names']

            if dataset_names == []:
                dataset_names += list(map(lambda i: i['headers']['name'],
                                    mongo_client.data_manager.datasets.find(dataset_query)))

            response_list = []
            for dataset_name in set(dataset_names):
                if len(dataset) != 0:
                    dataset = list(mongo_client.data[dataset_name].find())
                    if not os.path.isdir(f'{dataset_dir}'):
                        os.mkdir(f'{dataset_dir}')

                    json.dump(
                        json_tools.to_extended(dataset),
                        open(f'{dataset_dir}{dataset_name}db.json', mode='w+', encoding='utf-8'),
                        indent=4, ensure_ascii=False
                    )

                response_list.append({
                    'name': dataset_name,
                    'size': len(dataset),
                    'ok': len(dataset) != 0,
                })

            return {
                'ok': all([i['ok'] for i in response_list]),
                'datasets': response_list
            }
