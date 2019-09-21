import os
import logging

import attrdict
import colorlog
import yaml

from pymongo import MongoClient

with open("./config/settings.yml", 'r') as yamlfileobj:
    SETTINGS = attrdict.AttrDict(yaml.safe_load(yamlfileobj))

stream_handler = colorlog.StreamHandler()
stream_handler.setFormatter(colorlog.ColoredFormatter(
    '%(log_color)s%(levelname)-7s :[%(asctime)s][%(filename)15s:%(lineno)4s]:%(reset)s %(message)s',
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
