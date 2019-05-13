import logging
import pyyaml
import attrdict
from pymongo import MongoClient
from log4mongo.handlers import MongoHandler
from pprint import pprint


with open("./config/config.yml" , 'r') as yamlfileobj:
    config = attrdict.AttrDict(yaml.safe_load(yamlfileobj))


logging.basicConfig(
    datefmt='%y-%b-%d %H:%M:%S',
    format='%(levelname)8s:[%(asctime)s][%(filename)20s:%(lineno)4s -%(funcName)20s() ]: %(message)s',

    # datefmt='%H:%M:%S',
    level=logging.DEBUG,
    handlers=[
        # logging.FileHandler(f'{config.dir.project}/template_engine.log', mode='w+', encoding='utf8', delay=0),
        logging.StreamHandler(),
        MongoHandler(host=config.mongo.ip, port=config.mongo.port,
                     username=config.mongo.username, password=config.mongo.password,
                     authentication_db=config.mongo.authentication_db, database_name='TemplateManager', collection='log'),

    ]
)
logger = logging.getLogger('TemplateEngine')

mongo_client = MongoClient(
    f'mongodb://{config.mongo.username}:{config.mongo.password}@{config.mongo.ip}:{config.mongo.port}'
    f'/?authSource={config.mongo.authentication_db}')


def loggerHandle(loggerFunction, message, problemsList = None):
    if problemsList is not None:
        problemsList.append(message)
    
    loggerFunction(message)


# if CONFIG.use_mongo:
#     mongo = MongoClient('mongodb://localhost:27017')


