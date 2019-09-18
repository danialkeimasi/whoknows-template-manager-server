import os
import logging

import attrdict
import colorlog
import yaml
from pymongo import MongoClient

with open("./config/settings.yml", 'r') as yamlfileobj:
    CONFIG = attrdict.AttrDict(yaml.safe_load(yamlfileobj))

stream_handler = colorlog.StreamHandler()
stream_handler.setFormatter(colorlog.ColoredFormatter())

logging.basicConfig(
    datefmt='%y-%b-%d %H:%M:%S',
    format='%(levelname)8s:[%(asctime)s][%(filename)20s:%(lineno)4s -%(funcName)20s() ]: %(message)s',

    level=logging.DEBUG,
    handlers=[
        logging.FileHandler(os.path.join(CONFIG.dir.project, '__last.log'), mode='w+', encoding='utf8', delay=0),
        stream_handler,
    ]
)
logger = logging.getLogger('TemplateEngine')
logging.getLogger("matplotlib").setLevel(logging.WARNING)

mongo_client = MongoClient(CONFIG.mongo.uri)
