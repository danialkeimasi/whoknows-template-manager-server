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

    try:
        newTemplate.pop('__number')
        newTemplate.pop('number')
        newTemplate.pop('__id')
    except:
        pass
    

    newTemplate['__number'] = last_number + 1
    save_template(templates + [newTemplate])

def template_syntax_checker(template, problems = None):

    problems = [] if problems is None else problems

    if not ('__level' in template and 1 <= template['__level'] <= 10):
        problems.append(f"template must have a '__level' part in by this range: [1, 10]")

    if not('__usage' in template):
        problems.append(f"template must have a '__usage' part in it")

    if not('__values' in template):
        problems.append(f"template must have a '__values' part in it")

    question_types = [key for key in template.keys() if not key.startswith('__')]

    logger.critical(f'found this question types: {question_types}')

    template_formatter = json.load(open('templates\\template_v2\\template_formatter.json'))

    for qtype in question_types:
        if not(qtype in template_formatter):
            problems.append(f'there is an undefined question type in template: {qtype}')

        for question_property_name in template[qtype].keys():
            if not(question_property_name in template_formatter[qtype]):
                problems.append(f'there is an undefined part in "{qtype}" in template: {question_property_name}')

            question_property = template[qtype][question_property_name]
            if not(
                'format' in question_property and
                'content' in question_property and
                isinstance(question_property['format'], str) and
                isinstance(question_property['content'], list)
                ):
                problems.append(f"wrong syntax for {question_property_name} part in {qtype} question type")

        requirements = [item for item in
                        set(template_formatter[qtype].keys()) - set(template[qtype].keys()) if template_formatter[qtype][item]]
        if requirements:
            problems.append(f"there is no {requirements} in {qtype} type question")

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