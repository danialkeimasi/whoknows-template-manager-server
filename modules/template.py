from config.config import logger, CONFIG
import json
from pprint import pprint
import re
import pandas as pd
import os



class Template:

    template_formatter = json.load(open('templates\\template_v2\\template_formatter.json'))

    def __init__(self, template_dict):
        self.template = template_dict
        pass


    def check_json_format(self, problems = None):
        """
        check's the format of template json and
        if there is any problem
        returns it as a list
        :param problems:
        :return problems_list:
        """
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

        logger.critical(problems)
        return problems


    def get_required_data_names(self):
        """
        get's a list of databases names that required for template
        :return database name:
        """
        data_list = []
        data_regex = r'.*?db\(([a-zA-Z]*).*\).*?'

        for val in self.template['__values'].values():
            val = val.replace(' ', '')

            if re.search(data_regex, val):
                data_list.append(re.search(data_regex, val).group(1))

        return list(set(data_list))


    def check_data(self, problems = None):
        """
        check if necessary databases for this template is exist
        returns a list of problems
        if its empty we are fine
        :param problems:
        :return problems list:
        """
        problems = [] if problems is None else problems
        datasets = self.get_required_data_names()

        for ds_name in datasets:
            if not os.path.isfile(f'{CONFIG.dataset_dir}/{ds_name}db.json'):
                problems.append(f'dataset named "{ds_name}" not found in {CONFIG.dataset_dir}/ dir.')

        logger.critical(problems)
        return problems

    def find_tags(self, problems = None):
        problems = [] if problems is None else problems

        return problems



    def generate_question(self, tags=[], format={}, level=None, test_template=False):
        pass


