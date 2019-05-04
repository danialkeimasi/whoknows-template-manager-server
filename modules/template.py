from config.config import logger
import json
from pprint import pprint


class Template:


    template_formatter = json.load(open('templates\\template_v2\\template_formatter.json'))


    def __init__(self, template_dict):
        self.template = template_dict
        pass


    def check_format(self, problems = None):
        problems = [] if problems is None else problems

        template_consts = ['__level', '__usage', '__values', '__time',
                           '__score']
        for item in template_consts:
            if not (item in self.template):
                problems.append(f'template must have a "{item}" part in it')

        question_types = [key for key in self.template.keys() if not key.startswith('__')]
        logger.critical(f"found this question types: {question_types}")

        for q_type in question_types:
            if not (q_type in self.template_formatter):
                problems.append(f"there is an undefined question type in template: {q_type}")

            for q_property_name in self.template[q_type].keys():
                if not (q_property_name in self.template_formatter[q_type]):
                    problems.append(f'there is an undefined part in "{q_type}" type in template: {q_property_name}')

                q_property = self.template[q_type][q_property_name]
                if not (
                        'format' in q_property and
                        'content' in q_property and
                        isinstance(q_property['format'], str) and
                        isinstance(q_property['content'], list)
                ):
                    problems.append(f"wrong syntax for {q_property_name} part in {q_type} question type")

            q_requirements = [item for item in
                              set(self.template_formatter[q_type].keys()) - set(self.template[q_type].keys())
                              if self.template_formatter[q_type][item]]
            if q_requirements:
                problems.append(f"there is no {q_requirements} in {q_type} type question")

        pprint(problems)
        return problems



    def find_tags(self, problems = None):
        problems = [] if problems is None else problems


        return problems



    


