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

def template_syntax_checker(template):
    problems = []
    if not ('__level' in template and 1 <= template['__level'] <= 10):
        problems.append(f"there is problem with '__level'")

    if not('__usage' in template):
        problems.append(f"template must have a '__usage' part in it")

    if not('values' in template):
        problems.append(f"template must have a 'values' part in it")

    for item in ['writing', 'true_false', 'multichoices', 'selective']:
        if f"title_{item}" in template and not(f"answer"):
            pass

    pprint(template)


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