from config.config import logger, CONFIG
import json
from pprint import pprint
import re
import pandas as pd
import os
from modules.tools.data_container import DataContainer, db, listSub
import copy
from modules.tools.functions import choose, rand, to_list
from modules.question import Question


import random


class Template:

    __template_formatter = json.load(open('templates\\template_v2\\template_formatter.json'))

    __default_metadata = {
        'NOC': 3,
        'NOS': 4,
        'NOA': 2,
        'level': 1,
    }


    def __init__(self, template_dict):
        self.__template = template_dict
        pass

    def dict(self):
        return self.__template
    
    def get_question_types(self):
        return [key for key in self.__template.keys() if key.startswith('__')]


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
                           'idea', 'datasets']

        for item in template_consts:
            if not (item in self.__template):
                problems.append(f'template must have a "{item}" part in it')

        question_types = self.get_question_types()
        logger.critical(f"found this question types: {question_types}")

        for q_type in question_types:
            if not (q_type in self.__template_formatter):
                problems.append(f"there is an undefined question type in template: {q_type}")

            for q_property_name in self.__template[q_type].keys():
                if not (q_property_name in self.__template_formatter[q_type]):
                    problems.append(f'there is an undefined part in "{q_type}" type in template: {q_property_name}')

                q_property = self.__template[q_type][q_property_name]

            q_requirements = [item for item in
                              set(self.__template_formatter[q_type].keys()) - set(self.__template[q_type].keys())
                              if self.__template_formatter[q_type][item]]
            if q_requirements:
                problems.append(f"there is no {q_requirements} in {q_type} type question")

        logger.critical(problems)
        return problems


    def get_required_data_names_from_values(self):
        """
        get's a list of databases names that required for template
        :return database name:
        """
        data_list = []
        data_regex = r'.*?db\(([a-zA-Z]*).*\).*?'

        for val in self.__template['values'].values():
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

        datasets = self.__template['datasets']

        for ds_name in datasets:
            if not os.path.isfile(f'{CONFIG.dataset_dir}/{ds_name}db.json'):
                problems.append(f'dataset named "{ds_name}" not found in {CONFIG.dataset_dir}/ dir.')

        logger.critical(problems)
        return problems

    def parse(self, metadata, problems=[]):
        var = DataContainer()

        for key, value in metadata.items():
            setattr(var, key, value)

        # get the values to the "var"
        values_dict = {}
        for key, value in self.__template['values'].items():
            logger.info(f'{key} is going to eval')
            eval_result = eval(value)

            values_dict.update({key: eval_result})
            setattr(var, key, eval_result)

        template = copy.deepcopy(self.__template)
        template.update({'values': values_dict})

        q_type_names = Template(template).get_question_types()
        reg_str = r'[^`]*?`([^`]*?)`[^`]*?'

        for q_type_name in q_type_names:
            for q_property_name in template[q_type_name].keys():
                for q_property_format_name in template[q_type_name][q_property_name].keys():
                    for i, raw_str in enumerate(template[q_type_name][q_property_name][q_property_format_name]):

                        while re.search(reg_str, raw_str):
                            exp = re.search(reg_str, raw_str).group(1)
                            eval_result = eval(exp)
                            raw_str = raw_str.replace(f'`{exp}`',
                                                str(eval_result[0] if isinstance(eval_result, list) else eval_result))

                        template[q_type_name][q_property_name][q_property_format_name][i] = raw_str

        return Template(template)


    def get_question(self, question_type, format, problems = []):
        template = self.__template
        pprint(template[question_type])
        question = template[question_type]

        question.update({
            'question_type': question_type[2:],
            'tags': template['tags'],
            'usage': template['usage'],
            'values': template['values'],
            'datasets': template['datasets'],
            'problems': problems,
        })


        return Question(question)


    def generate_question(self, metadata={},
                          question_type=None, problems=[], format={},
                          test_template=False):

        self.__default_metadata['NOA'] = random.randint(0, 4)
        self.__default_metadata['level'] = random.randint(1, 11)

        for not_found_metadata_name in set(self.__default_metadata.keys()) - set(metadata.keys()):
            metadata[not_found_metadata_name] = self.__default_metadata[not_found_metadata_name]

        question_type = choose(self.get_question_types()) if question_type is None else f'__{question_type}'

        load_template_datasets(self.__template['datasets'])

        parsed_template = self.parse(metadata, problems)
        question_object = parsed_template.get_question(question_type, format, problems)

        return question_object.dict()



def load_data(dbname):
    '''
    Loads the given dataset and returns it

    Parameters
    ----------
    dbname : str
        name of dataset
    '''
    logger.info(f'dbname={dbname}')
    problems = []
    data = pd.DataFrame()

    for i in range(5):
        try:
            logger.info(f'trying to load {dbname} dataset from hard disk...')
            data = pd.DataFrame(json.load(open(f'{CONFIG.dataset_dir}/{dbname}db.json', encoding='utf-8')))
            logger.info(f'loading {dbname} dataset is done.')
            break
        except Exception as error:
            problems += [f'could not open dataset {dbname} from {CONFIG.dataset_dir} directory because {error}']

    logger.info(f'problems is {problems}')
    return data

def load_template_datasets(necesery_Dsets):
    logger.info(f'{necesery_Dsets}')

    for db in necesery_Dsets:
        globals()[db] = load_data(db)
