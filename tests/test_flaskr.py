from flask import json
from app import app


def test_generate_question():
    response = app.test_client().post(
        '/question/generate',
        json={'count': 5},
    )

    response_data = json.loads(response.get_data(as_text=True))

    assert 'ok' in response_data and 'questions' in response_data
    assert response_data['ok'] == True
