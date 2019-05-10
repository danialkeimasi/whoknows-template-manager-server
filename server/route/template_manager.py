from server.flask import getApp
from flask import json, request, render_template




def add():
    app = getApp()
    @app.route('/template_manager', methods=['GET'])
    def template_manager():

        return render_template('_pages/template_manager.html')
