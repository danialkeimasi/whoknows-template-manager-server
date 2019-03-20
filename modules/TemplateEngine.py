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
from modules.tools import choose, rand, to_list

from modules.checkTemplates import *
from modules.DataHelper import *
from modules.exceptions import *
from modules.checkTags import *
from modules.config import *



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
    

def parse(template , question , var, QT):
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


def get_templates_list(tags=[], numbers=[], sources=[]):
    '''
    Loads wanted tempaltes from file and return them as a list

    Parameters
    ----------
    tags : list
        specifies tags of wanted templates
    '''
    chosen_templates = []
    for template_file in glob.glob(f'{CONFIG.templates_dir}/*.json'):
        new_templates = json.load(open(template_file, encoding='utf-8'))
        for template in new_templates:
            template['source'] = template_file
        chosen_templates += new_templates
    
    if tags:
        chosen_templates = [x for x in chosen_templates if any((tag in find_tags(x)) for tag in tags)]
        
    if numbers:
        chosen_templates = [x for x in chosen_templates if x['__number'] in numbers]

    if sources:
        chosen_templates = [x for x in chosen_templates if any((x['source'].find(source) != -1) for source in sources)]
    
    # for template in templates:
    # 	if any('tags' in keys for keys in template):
    # 			for tag in tags:
    # 				if tag in template['tags']:
    # 					chosen_templates += [template]
    
    return chosen_templates


def test_templates(templates, try_count=5, rounds_count=1, save_result=True, debug=False):
    '''
    Inspect a template and generate question with it to check it's performance and find it's problems and return the results

    Parameters
    ----------
    template : dict
        wanted template to be inspected
    '''
    
    if not templates:
        raise TemplateTestFailed('There is no template to test!')
    
    questions = []
    templates_test = {}
    for template in templates:
        logger.info(f"\n{'*' * 80}\nTesting template number={template['__number']} source={re.sub('.*/', '', template['source'])} : \n{'-' * 40}\n")

        templates_test[template['__number']] = {
            'problems': []
        }

        logger.info(f"Testing template number : {template['__number']}")

        for _ in range(try_count):	
            question, problems = template_engine(template, debug=debug)
            questions += [question]
            if not problems:
                logger.info(f'SUCCESSFULL')
            
            for problem in problems:
                logger.error(problem)
                templates_test[template['__number']]['problems'] += problems

        logger.info(f"\n{'*' * 80}\n")
        if problems:
            logger.info(f'FAILED')

        json.dump(mongo_to_json(questions),
            open(f'{CONFIG.result_dir}/questions.json', 'w', encoding='utf-8'), indent=4, ensure_ascii=False)

    test_result = {
        'templates_count'	: len(templates),
        'success'			: len(set([question['__number'] for question in questions if not question['active']])),
        'fails'				: len(set([question['__number'] for question in questions if question['active']])),
        'success_rate'		: str(int(len([True for question in questions if question['active']]) / (len(templates) * try_count) * 100)) + '%',
        'failed_templates'	: sorted(list(set([question['__number'] for question in questions if not question['active']]))),
        'templates'			: [{
            '__number'		: template['__number'],
            'source'		: template['source'],
            'test_count'	: try_count,
            'success'		: len([True for question in questions if question['active'] and question['__number'] == template['__number']]),
            'fails'			: len([True for question in questions if not question['active'] and question['__number'] == template['__number']]),
            'success_rate'	: str(int(len([True for question in questions if question['active'] and question['__number'] == template['__number']]) / (try_count) * 100)) + '%',
            'time_avg'		: 0,
            'problems'		: [problem + f" *** count = {templates_test[template['__number']]['problems'].count(problem)}" for problem in list(set(templates_test[template['__number']]['problems']))],
        } for template in templates]
    }

    if save_result:
        json.dump(mongo_to_json(test_result), open(f'{CONFIG.result_dir}/test_result.json', 'w+', encoding='utf-8'), indent=4)

    logger.info(f'test_templates()\t-----> problems is {problems}')
    return test_result


def project_checkup():
    '''
    Checks every necessary part of project and CONFIGs to be ok and work fine and return the results
    
    TODO : check the template folder and templates and return the number of templates and ...
    TODO : check datasets
    '''
    checkup = {
        'templates': [],
        'datasets' : [],
    }
    for template_file in glob.glob(f'{CONFIG.templates_dir}/*.json'):
        templates = json.load(open(template_file, encoding='utf-8'))
        file_name = re.sub('.*/', '', template_file)
        checkup['templates'] += [{
            file_name: len(templates)
        }]
    
    for dataset_file in glob.glob(f'{CONFIG.dataset_dir}/*.json'):
        file_name = re.sub('.*/', '', dataset_file)
        error = ''
        
        try:
            dataset = json.load(open(dataset_file, encoding='utf-8'))
        except Exception as e:
            dataset = None
            error = e
        
        checkup['datasets'] += [{
            file_name: len(dataset) if dataset else f'0 ... Error while loadnig ---> {error}'
        }]
    return checkup


def arg_parse():
    '''
    command line interface
    '''
    parser = argparse.ArgumentParser(description='Process some integers.')

    parser.add_argument('--test', '--test_templates', nargs='*', type=int, dest='test',
                        default=False, help='test the templates and make questions')

    parser.add_argument('--checkup', dest='checkup', default=False, action='store_true',
                        help='checkup every necessary part of project to work fine')

    parser.add_argument('--debug', dest='debug', default=False, action='store_true',
                        help='specify debug flag in template_engine')

    parser.add_argument('-source', type=str, nargs='+', dest='source', default=False,
                        help='sources of templates to test')

    parser.add_argument('-count', type=int, default=5, dest='count',
                        help='number of test for each template')

    args = parser.parse_args()
    if args.checkup:
        logger.critical('Checkup results : ')
        logger.critical(json.dumps(project_checkup(), indent=4))
    
    if args.test != False:
        chosen_templates = get_templates_list(numbers=args.test, sources=args.source)
        test_result = test_templates(chosen_templates, try_count=args.count, debug=args.debug)
        logger.critical(json.dumps(test_result, indent=4))


def score_compare(answer, question, QT):
    '''
    Return if answer is correct or not
    '''
    #answer = question['answer']
    accept_rate = 70 if QT == 'writing' else 100
    ans = question['answer']
    if question['answer'] and QT == "true_false":
        ans = "True"
    elif QT == "true_false":
        ans = "False"
    print("similaaaaaaaary= " , similar(answer, ans)*100 , "accept_rate =   " , accept_rate)
    if (similar(answer, ans)*100 >= accept_rate ):
        return 1
    else:
        return 0

def similar(a,b):
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

    globals()['NOC'] = NOC
    
    problems += load_used_datasets(template)
    problems += check_template(template, QT) + check_global_constants(question)
    
    var = DataHelper()
    
    try:
        question = parse(template , question , var , QT)
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
    
    # out = [template_engine(qaleb, QT=typ) for typ in types]
    out = template_engine(qaleb, QT=types[0])
    # out = create_question('footballTeam', 1)
    
    print('\n---\n@output:')
    pprint(out)