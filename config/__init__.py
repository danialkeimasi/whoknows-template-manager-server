import logging
import colorlog
import yaml
import attrdict

from pymongo import MongoClient

with open("./config/settings.yml", 'r') as yamlfileobj:
    config = attrdict.AttrDict(yaml.safe_load(yamlfileobj))

stream_handler = colorlog.StreamHandler()
stream_handler.setFormatter(colorlog.ColoredFormatter())

logging.basicConfig(
    datefmt='%y-%b-%d %H:%M:%S',
    format='%(levelname)8s:[%(asctime)s][%(filename)20s:%(lineno)4s -%(funcName)20s() ]: %(message)s',

    level=logging.DEBUG,
    handlers=[
        logging.FileHandler(f'{config.dir.project}/config/last_run.log', mode='w+', encoding='utf8', delay=0),
        stream_handler,
    ]
)
logger = logging.getLogger('TemplateEngine')
logging.getLogger("matplotlib").setLevel(logging.WARNING)

mongo_client = MongoClient(
    f'mongodb://{config.mongo.username}:{config.mongo.password}@{config.mongo.ip}:{config.mongo.port}'
    f'/?authSource={config.mongo.authentication_db}')
