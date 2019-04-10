from server.flask import getApp
from flask import json, request

def add():
    app = getApp()
    @app.route('/test_template', methods=['GET'])
    def test_template():
        return 'mamad'