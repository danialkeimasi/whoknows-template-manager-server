from flask import Flask, request
import json
from pprint import pprint

# from template_engine.TemplateEngine import create_question, check_answer, get_templates_list
# from template_engine.TemplateEngine import TemplateEngine

app = Flask(__name__)

URLS_CONST = {
    'getQ':'getquestion', 
    'chkAns':'checkAnswer',
}


@app.route('/')
def main():
    Response = {
        'ok': 1,
        'message': 'question server is on',
        'urls': list(URLS_CONST.values()),
    }

    return json.dumps(Response)



@app.route(f'/{URLS_CONST["getQ"]}', methods=['POST', 'GET'])
def getquestion():
    Response = ''
    
    if request.method == 'POST':
        Request = request.json
        Response = Request
    
    elif request.method == 'GET':
        Response = {
            'ok': 0,
            'error': 'please use post request for get question',
            'request': {
                'tag': 'some tag that you want',
            }
        }
    
    return json.dumps(Response)


@app.route(f'/{URLS_CONST["chkAns"]}', methods=['POST', 'GET'])
def checkAnswer():
    Response = ''

    if request.method == 'POST':
        Request = request.json
        Response = Request
    
    elif request.method == 'GET':
        Response = {
            'ok': 0,
            'error': 'please use post request for check Ans',
            'request': {
                'id': 'question ID',
                'answer': 'answer or answers',
            }
        }
    
    return json.dumps(Response)



if __name__ == '__main__':
    app.debug = True
    app.run()