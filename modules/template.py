from config.config import logger, CONFIG
import json
from pprint import pprint
import re
import pandas as pd
import os
from modules.tools.data_container import DataContainer
import copy


class Template:

    template_formatter = json.load(open('templates\\template_v2\\template_formatter.json'))

    def __init__(self, template_dict):
        self.template = template_dict
        pass

    
    def get_question_types(self):
        return [key for key in self.template.keys() if key.startswith('__')]


    def check_json_format(self, problems=[]):
        """
        check's the format of template json and
        if there is any problem
        returns it as a list
        :param problems:
        :return problems_list:
        """

        template_consts = ['level', 'usage', 'values', 'time_function',
                           'score_function', 'tags', 'state', 'state_info',
                           'idea']

        for item in template_consts:
            if not (item in self.template):
                problems.append(f'template must have a "{item}" part in it')

        question_types = self.get_question_types()
        logger.critical(f"found this question types: {question_types}")

        for q_type in question_types:
            if not (q_type in self.template_formatter):
                problems.append(f"there is an undefined question type in template: {q_type}")

            for q_property_name in self.template[q_type].keys():
                if not (q_property_name in self.template_formatter[q_type]):
                    problems.append(f'there is an undefined part in "{q_type}" type in template: {q_property_name}')

                q_property = self.template[q_type][q_property_name]

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

        for val in self.template['values'].values():
            val = val.replace(' ', '')

            if re.search(data_regex, val):
                data_list.append(re.search(data_regex, val).group(1))

        return list(set(data_list))


    def check_data(self, problems=[]):
        """
        check if necessary databases for this template is exist
        returns a list of problems
        if its empty we are fine
        :param problems:
        :return problems list:
        """

        datasets = self.get_required_data_names()

        for ds_name in datasets:
            if not os.path.isfile(f'{CONFIG.dataset_dir}/{ds_name}db.json'):
                problems.append(f'dataset named "{ds_name}" not found in {CONFIG.dataset_dir}/ dir.')

        logger.critical(problems)
        return problems

    def parse(self, problems=[]):
        var = DataContainer()
        age = 15
        # get the values to the "var"
        for key, value in self.template['values'].items():
            logger.info(f'{key} is going to eval')
            setattr(var, key, eval(value))

        template = copy.deepcopy(self.template)
        q_type_names = Template(template).get_question_types()

        for q_type_name in q_type_names:
            for q_property_name in template[q_type_name].keys():
                for q_property_format_name in template[q_type_name][q_property_name].keys():
                    raw_str = template[q_type_name][q_property_name][q_property_format_name]
                    reg_str = r'[^`]*?`([^`]*?)`[^`]*?'
                    while re.search(reg_str, raw_str):
                        exp = re.search(reg_str, raw_str).group(1)
                        eval_result = eval(exp)
                        raw_str = raw_str.replace(f'`{exp}`',
                                                  str(eval_result[0] if isinstance(eval_result, list) else eval_result))

                    template[q_type_name][q_property_name][q_property_format_name] = raw_str

        return template
        # for q_type in self.template[q_types].keys():
        #     for q_property in self.template[q_type]:
        #         for q_property_format in q_property:
        #             print(q_property_format)


    def generate_question(self, NOC , question_type=None, problems=[], format={},
                          level=None, test_template=False):
        pass

