import logging
from pymongo import MongoClient


class CONFIG:
    """
    Configurations and settings of project

    TODO : should use a config file to load it
    """
    
    debug = not True
    project_dir = 'D:/Programming/Python/whoKnows/guessit-question-manager'
    templates_dir = f'{project_dir}/modules/templates'
    questions_dir = f'{project_dir}/modules'
    result_dir = f'{project_dir}/template_engine/result'
    dataset_dir = f'{project_dir}/../datasets'
    language = 'fa'
    use_mongo = False


datasets = ['movie', 'director', 'song', 'actor', 'footballPlayer', 'footballTeam', 'quote',
            'country', 'book', 'name', 'word', 'volleyballTeam']  # should be done automatically by searching db_directory

logging.basicConfig(
    format='### %(asctime)s - %(levelname)-8s : %(message)s \n',
    # datefmt='%H:%M:%S',
    datefmt='%H:%M',
    level=logging.NOTSET,
    handlers=[
        #logging.FileHandler(f'{CONFIG.project_dir}/template_engine.log', mode='w+', encoding='utf8', delay=0),
        logging.StreamHandler(),
    ]
)

logger = logging.getLogger('TemplateEngine')

if CONFIG.use_mongo:
    mongo = MongoClient('mongodb://localhost:27017')

