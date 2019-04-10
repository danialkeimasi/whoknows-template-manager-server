from server.flask import getApp
from flask import json, request
from modules.TemplateEngine import testTemplate_ByCreate_Question


def add():
    app = getApp()
    @app.route('/test_template', methods=['POST'])
    def test_template():
        
        Request = request.json

        # TODO: this function just return the question that we make
        Out = testTemplate_ByCreate_Question(Request)
        
        return json.dumps(Out)
