from flask import json

from config import mongo_client
from app import app

from modules.tools import json_tools


def test_question_generate():
    response = app.test_client().post(
        '/question/generate',
        json={'count': 10},
    )

    response_data = json.loads(response.get_data(as_text=True))

    assert 'ok' in response_data and 'questions' in response_data
    assert response_data['ok']



# def test_shell():
#     template_id = json_tools.to_extended(list(mongo_client.template_manager.templates.aggregate([
#                 {'$match': {'__state': 'in_use'}},
#                 {'$sample': {'size': 1}}
#             ]))[0]['_id'])['$oid']

#     response = app.test_client().post(
#         '/shell',
#         json={'command': f'test -t {template_id}'},
#     )
#     response_data = json.loads(response.get_data(as_text=True))
#     assert 'response' in response_data
#     assert response_data['response'] != []



# def test_template_test():
#     response = app.test_client().post(
#         '/template/test',
#         json={
#             'template': list(mongo_client.template_manager.templates.aggregate([
#                 {'$match': {'__state': 'in_use'}},
#                 {'$sample': {'size': 1}}
#             ]))[0]
#         }
#     )

#     response_data = json.loads(response.get_data(as_text=True))

#     assert 'ok' in response_data
#     assert response_data['ok']
#     assert response_data['template']['__state'] == 'in_use'

