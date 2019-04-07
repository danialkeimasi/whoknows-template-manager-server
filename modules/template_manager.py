import json
import glob
import functools
from config import CONFIG
import sys


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
            

def addTemplate(f):
    
    def save_template(template):
        with open(f'{CONFIG.questions_dir}/templates_seprated/{fileName}_{template["__number"]}.json', 'w+') as f:
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

    
if __name__ == "__main__":
    # separator()

    f = sys.argv[1]
    addTemplate(f)