import json
import glob
import sys
import requests
import functools
from pprint import pprint
from modules.Config import CONFIG, logger


def separator():
    def item(f):
        templates = json.load(open(f))
        for template in templates:
            
            template['__file'] = f[f.rindex('\\')+1:f.rindex('.')]
        return templates

    template_files = glob.glob(f'{CONFIG.templates_dir}/*.json')
    templates = functools.reduce(lambda a, b: a + b, map(item, template_files))

    for i, template in enumerate(templates):
        fileName = template["__file"]
        template.pop('__file')
        with open(f'{CONFIG.questions_dir}/templates_seprated/{fileName}_{template["__number"]}.json', 'w+') as f:
            json.dump(template, f, indent=4, separators=(',', ': '), ensure_ascii=False)
            

def addTemplate_toMainJson(f):
    
    def save_template(template):
        with open(f'{CONFIG.questions_dir}/templates_seprated/{template["__number"]}.json', 'w+') as f:
            json.dump(template, f, indent=4, separators=(',', ': '), ensure_ascii=False)

    '''
    param:
        - json file of a template
    
    add the given template to the templates
    '''

    templates = json.load(open(f'{CONFIG.templates_dir}/template.json'))
    last_number = max([template['__number'] for template in templates] + [0])
    
    newTemplate = json.load(open(f))
    

    newTemplate['__number'] = last_number + 1
    save_template(templates + [newTemplate])

def template_syntax_checker(template, problems = None):
    problems = [] if problems is None else problems

    template_consts = ['__level', '__usage', '__values', '__time',
                       '__score']
    for item in template_consts:
        if not(item in template):
            problems.append(f"template must have a '{item}' part in it")

    question_types = [key for key in template.keys() if not key.startswith('__')]
    logger.critical(f'found this question types: {question_types}')

    template_formatter = json.load(open('templates\\template_v2\\template_formatter.json'))

    for q_type in question_types:
        if not(q_type in template_formatter):
            problems.append(f'there is an undefined question type in template: {q_type}')

        for q_property_name in template[q_type].keys():
            if not(q_property_name in template_formatter[q_type]):
                problems.append(f'there is an undefined part in "{q_type}" in template: {q_property_name}')

            q_property = template[q_type][q_property_name]
            if not(
                'format' in q_property and
                'content' in q_property and
                isinstance(q_property['format'], str) and
                isinstance(q_property['content'], list)
                ):
                problems.append(f"wrong syntax for {q_property_name} part in {q_type} question type")

        q_requirements = [item for item in
                        set(template_formatter[q_type].keys()) - set(template[q_type].keys()) if template_formatter[q_type][item]]
        if q_requirements:
            problems.append(f"there is no {q_requirements} in {q_type} type question")

    pprint(problems)
    return problems

def add_template_to_server(template):
    '''
    add the given template address to the templates in mongo
    HOW TO RUN:
        this function run's by this command:
            python app.py --addTemplate <template_address>

    - first load the template file
    - test all tags by templateEngine function and save the tags that can make question with them
    - do some improvement to template file and add the template to the database

    '''
    logger.critical('adding template to the server ...')

    template_syntax_checker(template)


    # response = requests.post(CONFIG.template_new, json=template)
    # return response