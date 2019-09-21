import os
from glob import glob
from os.path import basename

import flask_restplus
from flask import json

from config import mongo_client, SETTINGS, logger
from modules.tools import json_tools

parser = flask_restplus.reqparse.RequestParser()
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
            args = parser.parse_args()
            dataset_query = args['query']

            logger.critical(f'dataset_query: {dataset_query}')

            dataset_names = list(map(lambda i: i['headers']['name'],
                                     mongo_client.data_manager.datasets.find(dataset_query)))

            logger.critical(f'dataset_names that we found: {dataset_names}')

            response_list = []
            for dataset_name in dataset_names:
                dataset = list(mongo_client.data[dataset_name].find())
                if len(dataset) != 0:
                    if not os.path.isdir(SETTINGS.dir.dataset):
                        os.mkdir(SETTINGS.dir.dataset)

                    json.dump(
                        json_tools.to_extended(dataset),
                        open(os.path.join(SETTINGS.dir.dataset, f'{dataset_name}db.json'), mode='w+', encoding='utf-8'),
                        indent=4, ensure_ascii=False
                    )

                response_list.append({
                    'name': dataset_name,
                    'size': len(dataset),
                    'ok': len(dataset) != 0,
                })

            datasets_in_data_manager = list(map(lambda i: i['headers']['name'],
                                                mongo_client.data_manager.datasets.find(dataset_query)))

            for file in [basename(path).split('.')[0] for path in glob(f'{SETTINGS.dir.dataset}/*')]:
                if file[:-2] not in datasets_in_data_manager:
                    os.remove(os.path.join(SETTINGS.dir.dataset, f'{file}.json'))

            final_response = {
                'ok': all([i['ok'] for i in response_list]),
                'updated_datasets': response_list,
                'problems': [
                    f"there is some problem with '{dataset['name']}' dataset" for dataset in response_list if
                    not dataset['ok']
                ],
            }

            logger.critical(f'final_response: {final_response}')
            return final_response
