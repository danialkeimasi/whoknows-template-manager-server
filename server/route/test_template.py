from server.flask import getApp
from flask import json, request


def add():
    app = getApp()
    @app.route('/test_template', methods=['POST'])
    def test_template():
        
        Request = request.json

        # TODO: this function just return the question that we make
        
        return json.dumps(Out)
