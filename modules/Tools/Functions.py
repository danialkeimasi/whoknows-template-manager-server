import random
import glob
import json
import re

from modules.Tools.Exceptions import *
from modules.Config import logger
from modules.Config import CONFIG


def rand(needList, count=0, exceptions=[]):
    '''
	Return a list of random numbers in range of [start , ... , end], Returns only one number(not list) of count is not given
	Parameters
	----------
	needList   : list
        a list of items that we want to choose from
	count      : int
		number of random numbers that is needed
	exceptions : list
		list of numbers which is needed to be excluded from range
	'''

    for item in ['needList', 'exceptions']:
        if (not isinstance(locals()[item], list) and not isinstance(locals()[item], range)):
            raise ValueError(f'rand(): wrong type for {item} - you use {type(locals()[item])}')

    if len(needList) - len(exceptions) < count:
        raise ValueError(f'rand(): error- you choose {count} from {len(needList) - len(exceptions)}')

    needList = [i for i in needList if i not in exceptions]
    # needList = list(set(needList) - set(exceptions))

    choicesList = random.sample(range(len(needList)), 1 if count == 0 else count)

    resultList = [needList[i] for i in choicesList]
    return resultList[0] if count == 0 else resultList


def choose(items, count=0):
    '''
    Return a random sebset of given items with length of count as a list(returns only one item if count is None, Not as a list)

    Parameters
    ----------
    items : list
        a list of items that we want to choose from
    count : int
        number of random numbers that is needed
    '''
    return rand(needList=items, count=count)


def to_list(data):
    '''
    if data is not a list, return it as a list
    '''
    return data if isinstance(data, list) else [data]


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


def project_checkup():
    '''
    Checks every necessary part of project and CONFIGs to be ok and work fine and return the results

    TODO : check the template folder and templates and return the number of templates and ...
    TODO : check datasets
    '''
    checkup = {
        'templates': [],
        'datasets': [],
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
            question = template_engine(template, debug=debug)
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
        'templates_count': len(templates),
        'success'		: len(set([question['__number'] for question in questions if not question['active']])),
        'fails'				: len(set([question['__number'] for question in questions if question['active']])),
        'success_rate'		: str(int(len([True for question in questions if question['active']]) / (len(templates) * try_count) * 100)) + '%',
        'failed_template'	: sorted(list(set([question['__number'] for question in questions if not question['active']]))),
        'templates'			: [{
            '__number'		: template['__number'],
            'source'		: template['source'],
            'test_coun'	: try_count,
            'success'		: len([True for question in questions
                            if question['active'] and question['__number'] == template['__number']]),
            'fails'			: len([True for question in questions
                          if not question['active'] and question['__number'] == template['__number']]),
            'success_rat'	: str(int(len([True for question in questions
                                         if question['active'] and question['__number'] == template['__number']]) / (try_count) * 100)) + '%',
            'time_avg'		: 0,
            'problems'		: [problem + f" *** count = {templates_test[template['__number']]['problems'].count(problem)}" for problem in list(set(templates_test[template['__number']]['problems']))],
        } for template in templates]
    }

    if save_result:
        json.dump(mongo_to_json(test_result), open(f'{CONFIG.result_dir}/test_result.json', 'w+', encoding='utf-8')
                  , indent=4)

    logger.info(f'test_templates()\t-----> problems is {problems}')
    return test_result
