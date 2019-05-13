import logging
import pyyaml
import attrdict
from pymongo import MongoClient
from pprint import pprint

with open("./config/config.yml" , 'r') as yamlfileobj:
    config = attrdict.AttrDict(yaml.safe_load(yamlfileobj))


class CONFIG:
    """
    Configurations and settings of project

    TODO : should use a config file to load it
    """

    debug = not True
    project_dir = '.'
    templates_dir = f'{project_dir}/templates/main'
    questions_dir = f'{project_dir}/modules'
    result_dir = f'{project_dir}/template_engine/result'
    dataset_dir = f'{project_dir}/_datasets'
    language = 'fa'
    use_mongo = False

    main_server_ip = 'https://31.184.132.183:30000'
    template_new = f'{main_server_ip}/template/new'


datasets = ['movie', 'director', 'song', 'actor', 'footballPlayer', 'footballTeam', 'quote',
            'country', 'book', 'name', 'word',
            'volleyballTeam']  # should bea done automatically by searching db_directory

logging.basicConfig(
    datefmt='%y-%b-%d %H:%M:%S',
    format='%(levelname)8s:[%(asctime)s][%(filename)20s:%(lineno)4s -%(funcName)20s() ]: %(message)s',

    # datefmt='%H:%M:%S',
    level=logging.DEBUG,
    handlers=[
        # logging.FileHandler(f'{CONFIG.project_dir}/template_engine.log', mode='w+', encoding='utf8', delay=0),
        logging.StreamHandler(),
    ]
)

logger = logging.getLogger('TemplateEngine')

def loggerHandle(loggerFunction, message, problemsList = None):
    if problemsList != None:
        problemsList.append(message)
    
    loggerFunction(message)


# if CONFIG.use_mongo:
#     mongo = MongoClient('mongodb://localhost:27017')


