import pandas as pd
import random
import re
import json
import multiprocessing as mp
import os

from pprint import pprint
import copy
import glob
import argparse
import itertools
from difflib import SequenceMatcher
import functools

from tools import choose, rand, to_list

from checkTemplates import *
from DataHelper import *
from exceptions import *
from checkTags import *
from config import *
from argParse import arg_parse


def find_format(data):
    '''
    Finds the format of given data, if it's a link then returns link's format else text
    
    P-S:
        If data is a list by self (more than one item),
        We know that all of them have same format,
        So, we just find the format of first one.
    
    Formats
        image : png, jpg, jpeg, gif
        audio : mp3
        video : mp4

        Examples :
                "http://www.host.com/image.jpg" ---> image
                "http://www.host.com/audio.mp3" ---> audio
    '''
    data = to_list(data)

    if len(data) == 0:
        return 'none'

    val = str(data[0])
    if any([val.lower().find(f) != -1 for f in ['.png', '.jpg', '.jpeg', '.gif']]):
        return 'image'
    if any([val.lower().find(f) != -1 for f in ['.mp3']]):
        return 'audio'
    if any([val.lower().find(f) != -1 for f in ['.mp4']]):
        return 'video'
    else:
        return 'text'


def mongo_to_json(list_of_objects):	
    '''
    Converts MongoDB's ID objects to str so it can be json serializable
    '''
    list_of_objects = to_list(list_of_objects)

    for obj in list_of_objects:
        for key in obj:
            if str(type(obj[key])) == "<class 'bson.objectid.ObjectId'>":
                obj[key] = str(obj[key])

    return list_of_objects


def load_data(dbname):
    '''
    Loads the given dataset and returns it
    
    Parameters
    ----------
    dbname : str
        name of dataset
    '''
    logger.info(f'def load_data(dbname={dbname})')
    problems = []
    data = pd.DataFrame()

    while 'run_to_break':
        try:
            logger.info(f'trying to load {dbname} dataset from hard disk...')
            data = pd.DataFrame(json.load(open(f'{CONFIG.dataset_dir}/{dbname}db.json', encoding='utf-8')))
            logger.info(f'loading {dbname} dataset is done.')
            break
        except Exception as error:
            problems += [f'could not open dataset {dbname} from {CONFIG.dataset_dir} directory because {error}']

    logger.info(f'load_data()\t\t-----> problems is {problems}')
    return data


def used_datasets(template):
    '''
    Returns a list of used datasets in the given template

    Parameters
    ----------
    template : dict
        template that it's datasets are needed
    '''

    if 'values' not in template:
        logger.info('used_datasets()\t\t-----> no value')
        return []

    used_datasets = []
    for val in template['values'].values():
        if re.search(r'.*?db\(([a-zA-Z]*).*\).*?', val):
            dbname = re.search(r'.*?db\(([a-zA-Z]*).*\).*?', val).group(1)
            logger.info(f'used_datasets()\t\t-----> {dbname}')
            used_datasets.append(dbname)
    
    return list(set(used_datasets))


def db(doc, count=0):
    '''
    Gets a panada's Dataframe(doc) and randomly choose count number of items from dataframe and returns the data as a list of dicts

    Parmeters
    ----------
    doc : dataframe
        dataframe that we want to choose from
    count : int
        number of items which is needed (default is 1)
    '''

    logger.info(f'db(): count={count}')

    try:
        if len(doc.index) < (count if count != 0 else 1):
            logger.info(f'not enough data for db function to choose from, len(doc)={len(doc)} < count={count}')
            raise NotEnoughtData(f'not enough data for db function to choose from, len(doc)={len(doc)} < count={count}')

        data = doc.sample(count if count != 0 else 1)

    except Exception as error:
        logger.error(f'def db => {error}')
        return []

    data = data.to_dict('records')
    logger.info(f'def db => done')
    
    return DataHelper(data[0] if count == 0 else data)


def find_tags(template, question={}):
    '''
    Returns related tags for given template

    Parameters
    ----------
    template : dict
        wanted template to be checked
    question : dict
        ***
    '''
    tags = ['movie', 'music']
    founded_tags = []
    if 'tags' in template:
        founded_tags += template['tags']

    founded_tags += used_datasets(template)

    for tag in tags:
        if f'check_tag_{tag}' in globals() and globals()[f'check_tag_{tag}'](template, question):
            founded_tags += [tag]

    founded_tags  = list(set(founded_tags))
    return founded_tags
    

def parse(template , question , var, QT, NOC):
    problems = []
    for section in ['__usage' , '__number' , '__level']:
        setattr(var, section, template[section])


    if 'values' in template:
        for key, value in template['values'].items():
            logger.info(f'{key} is going to eval')
            setattr(var, key, eval(value))
        
            
    for section in ['title']:
        templateSec = section + '_' + QT
        
        if templateSec in template:
            question[section] = choose(template[templateSec])
            
            ra = ''
            if QT == "true_false":
                ra = (rand(range(1, len(template[templateSec])//2 + 1) ) -1) * 2 + int(not var.True_or_False)
                question[section] = template[templateSec][ra]

            
            regStr = r'[^`]*?`([^`]*?)`[^`]*?'
            while re.search(regStr, question[section]):
                exp = re.search(regStr, question[section]).group(1)
                question[section] = question[section].replace(f'`{exp}`', eval(exp)[0]) 
        else:
            logger.info(question)
            raise NoTitle(f'Wrong Type (QT) For Template in parse(), {templateSec} not found in template.')


    for section in ['answer']:
        templateSec = section + '_' + QT
    
        if templateSec in template:
            question[section] = eval(template[templateSec][0])
        else:
            logger.info(question)
            raise WrongTypeForTemplate(f'Wrong Type For Template in parse(), {templateSec} not found in template.')


    for section in ['choices']:
        templateSec = section + '_' + QT
    
        if templateSec in template:
            question[section] = eval(template[templateSec][0])
        else:
            if QT in ['multichoices', 'selective']:
                logger.info(question)
                raise WrongTypeForTemplate(f'Wrong Type For Template in parse(), {templateSec} not found in template.')


    for section in ['subtitle']:
        templateSec = section

        if templateSec in template:
            question[section] = eval(template[templateSec][0])
        else:
            question[section]= []


    if templateSec != "choices_true_false" and QT != "true_false" and templateSec != "subtitle": problems += f"{templateSec} is empty"
    logger.info(f'parse()\t\t\t-----> problems is {problems}')
    return question


def create_question(tags, question_count, subtitle_types=['audio', 'video', 'text', 'empty']):
    '''
    Create questions based on given tags and conditions

    Parameters
    ----------
    tags : list
        tags of wanted questions
    question_count : int
        number of wanted questions
    subtitle_type : list
        specify valid subtitle_type s for wanted questions
    '''


    templates = functools.reduce(lambda a, b: a + b, map(lambda f: json.load(open(f)), glob.glob(f'{CONFIG.templates_dir}/*.json')))
    
    questions = [template_engine(templates[0]) for i in range(question_count)]
    
    return questions


def score_compare(answer, question, QT):
    '''
    Return if answer is correct or not
    '''
    
    accept_rate = 70 if QT == 'writing' else 100
    ans = question['answer']

    sim = similar(answer, ans) * 100

    print(f'similarity= {sim}, accept_rate = {accept_rate}')
    return similar(answer, ans)*100 >= accept_rate


def similar(a,b):
    if not isinstance(a, str): a = str(a)
    if not isinstance(b, str): b = str(b)
    return SequenceMatcher(None, a, b).ratio()


def load_used_datasets(template):
    list_ = used_datasets(template)
    logger.info(f'load_used_datasets()\t-----> {list_}')
    
    for x in list_:
        globals()[x] = load_data(x)
    
    return []

def template_engine(template, NOC=3, NOS=4 , TIME=10, SCORE=100, QT=None, debug=False, reload_question=False, data_id=[]):
    '''
    Generate a question with the given template and conditions
    
    Parameter
    ---------
    template : dict
        template of question
    NOC : int
        number of choices
    ILMIN : int
        minimum of internal level
    ILMAX : int
        maximum of internal level
    NOS : int
        number of subtitles
    QT : str
        type of question
    reload_question : bool
        specify whether question should be generated with random data or given data id's (default is False)
    data_id : list
        data id's that should be used for reloading question if reload_question is True
    '''
    
    if QT == None:
        QT= rand(['multichoices', 'writing', 'true_false', 'selective'])

    logger.info(f'template_engine()\t-----> QT: {QT}')
    problems = []
    question = {
        'QuestionType' : QT,
        'NOC'		   : NOC,
        'NOS'		   : NOS,
        'active'	   : True,
        '__number'	   : template['__number'] if '__number' in template else - 1,
        'templateID'   : str(template['_id']) if '_id' in template else -1,
        'TIME'		   : TIME,
        'SCORE'		   : SCORE
    }

    problems += load_used_datasets(template)
    problems += check_template(template, QT) + check_global_constants(question)    
    var = DataHelper()
    
    try:
        question = parse(template , question , var , QT, NOC)
    
    except NoTitle as error:
        logging.info(error)
        question['active'] = False
        question['problems'] = problems
        return question

    question['answer_type'] = find_format(question['answer'])
    question['subtitle_type'] = find_format(question['subtitle']) if 'subtitle' in question else 'empty'
    question['tags']  = find_tags(template, question)
    problems += check_question(question ,QT)
    
    if problems:
        question['active'] = False
        question['problems'] = problems
    else:
        question['active'] = True

    logger.info(f'template_engine()\t-----> problems is {problems}')
    
    ans = 'maret'
    question['score'] = score_compare(ans , question , QT) 	
    
    question['TIME'] += 4 if len(question['title']) > 100 else \
    3 if len(question['title']) > 80 else  \
    2 if len(question['title']) > 60 else  \
    1 if len(question['title']) > 40 else 0	
    
    if question['subtitle']:  
        if find_format(question['subtitle'])   == 'video': question['TIME'] +=4
        elif find_format(question['subtitle']) == 'audio': question['TIME'] +=4	
        elif find_format(question['subtitle']) == 'image': question['TIME'] +=2	
    
    question['problems'] = problems
    return question


if __name__ == '__main__':
    arg_parse()
    qaleb = [x for x in json.load(open(f'{CONFIG.templates_dir}/footballTeam,league.json'))if x['__number']==1][0]

    print('\n---\n@input_Template:')
    pprint(qaleb)

    print('\n---\n@funcRun:')

    types = ['multichoices', 'writing', 'true_false', 'selective']
    
    out = [template_engine(qaleb, QT=typ) for typ in types]
    # out = template_engine(qaleb, QT=types[0])
    # out = create_question('footballTeam', 1)
    
    print('\n---\n@output:')
    pprint(out)