import os
import logging

import attrdict
import colorlog
import yaml

from pymongo import MongoClient
from environs import Env, EnvError


environment_variables = Env()
environment_variables.read_env()


try:
    ENV = environment_variables("ENV").lower()
except EnvError:
    ENV = 'debug'


SETTING_FILES = {
    'production': './config/profile-production.yml',
    'debug': './config/profile-debug.yml'
}


with open('./config/settings.yml', 'r') as yamlfileobj:
    SETTINGS = attrdict.AttrDict(yaml.safe_load(yamlfileobj))


with open(SETTING_FILES[ENV], 'r') as yamlfileobj:
    SETTINGS.update(attrdict.AttrDict(yaml.safe_load(yamlfileobj)))


stream_handler = colorlog.StreamHandler()
stream_handler.setFormatter(colorlog.ColoredFormatter(
    '%(log_color)s%(levelname)-8s:[%(asctime)s][%(filename)20s:%(lineno)3s ~%(funcName)15s()]:%(reset)s %(message)s',
    datefmt='%m-%d %H:%M:%S',
    style='%'
))


logging.basicConfig(
    level=logging.DEBUG,
    handlers=[
        logging.FileHandler(os.path.join(SETTINGS.dir.project, '__last.log'), mode='w+', encoding='utf8', delay=0),
        stream_handler,
    ]
)


logger = logging.getLogger('tms')
logging.getLogger("matplotlib").setLevel(logging.WARNING)


mongo_client = MongoClient(SETTINGS.mongo.uri)
