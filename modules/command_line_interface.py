import os
import sys
import json
import click
import unittest

from pprint import pprint
from modules.template import Template
from config import mongo_client, logger

from importlib import import_module
from os.path import basename
from glob import glob

from flask import Flask
from flask_cors import CORS
from flask_restplus import Api

from bson.objectid import ObjectId
from modules.template import Template


app = Flask(__name__)
api = Api(app)
CORS(app)

for file in [basename(path).split('.')[0] for path in glob('./routes/*.py') if not basename(path).startswith('__')]:
    import_module(f'routes.{file}').add(api)


@click.group()
def cli():
    pass


@cli.command()
@click.option('--host', '-h', default="0.0.0.0", help="the host that you want to run the server.")
@click.option('--port', '-p', default="3001", help="the port that you want to run the server.")
@click.option('--debug', '-d', default=False, is_flag=True, help="flask debug mode.")
def runserver(host, port, debug):
    global app

    app.run(debug=debug, host=host, port=port)


@cli.command()
@click.option('--template', '-t', required=True , help="the template oid.")
def generate(template):
    template = mongo_client.template_manager.templates.find_one({'_id': ObjectId(template)})
    question_dict = Template(template).generate_question().dict()
    pprint(question_dict)


@cli.command()
@click.option('--template', '-t', required=True , help="the template oid.")
def test(template):
    template = mongo_client.template_manager.templates.find_one({'_id': ObjectId(template)})
    template_updated_dict = Template(template).test_update().dict()
    pprint(template_updated_dict)


@cli.command()
@click.argument('command', type=str)
@click.option('--template', '-t', required=True , help="the template oid.")
def run(command, template):
    template = mongo_client.template_manager.templates.find_one({'_id': ObjectId(template)})
    response = Template(template).parse(run_command=command)
    pprint(response)
