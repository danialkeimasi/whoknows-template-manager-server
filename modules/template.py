import copy
import json
import os
import random
import re

import pandas as pd

from config.config import logger, mongo_client, ListHandler, config
from modules.question import Question
from modules.tools.data_container import DataContainer, db, listSub
from modules.tools.functions import choose, rand, to_list


class Template:
    __template_formatter = json.load(open(config.dir.template_formatter))
    __empty_template = json.load(open(config.dir.empty_template))
    
    __default_metadata = {
        'NOC': 3,
        'NOS': 4,
        'NOA': 2,
        'level': 1,
    }

    def __init__(self, inp, debug=False, mode='dict'):
        """
        check template structure if debug is true
        :param inp: template
        :param debug:
        """

        self.__template = json.load(open(inp, encoding='utf8')) if mode == 'file' else \
            inp if mode == 'dict' else \
                None

        self.__problems = []
        self.__template['__test_info'] = self.__empty_template['__test_info']

        if debug:
            self.__test_structure()
            self.__test_data()

    def dict(self):
        """
        :return template as dict:
        """
        return self.__template

    def problems(self):
        """
        :return problems of a template as dict:
        """
        return self.__problems

    def __update_problems(self, problems):
        """
        internal function for updating problems
        :param new problems:
        """
        self.__problems += [problem for problem in problems if problem not in self.__problems]

    def get_question_types(self):
        """
        get all the question types that can make with the template
        :return list of question types:
        """
        return [key for key in self.__template.keys() if key.startswith('&')]

    def parse(self, bool_answer=True, metadata={}):
        """
        eval the variables in the template with data that we have in datasets
        and return a new template object that has no variable in sentences
        :param metadata:
        :return Template:
        """

        load_template_datasets(self.__template['datasets'])

        self.__default_metadata['NOA'] = random.randint(0, 4)
        self.__default_metadata['level'] = random.randint(1, 11)

        for not_found_metadata_name in set(self.__default_metadata.keys()) - set(metadata.keys()):
            metadata[not_found_metadata_name] = self.__default_metadata[not_found_metadata_name]

        problems = []
        var = DataContainer()
        setattr(var, 'bool_answer', bool_answer)

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
        # template.update({'values': values_dict})

        q_type_names = Template(template).get_question_types()
        reg_str = r'[^`]*?`([^`]*?)`[^`]*?'

        for q_type_name in q_type_names:
            for q_property_name in template[q_type_name]:
                for q_property_format_name in template[q_type_name][q_property_name]:
                    for i, raw_str in enumerate(template[q_type_name][q_property_name][q_property_format_name]):

                        if raw_str.startswith('$'):
                            template[q_type_name][q_property_name][q_property_format_name] = to_list(eval(raw_str[1:]))

                        else:
                            while re.search(reg_str, raw_str):
                                exp = re.search(reg_str, raw_str).group(1)
                                eval_result = eval(exp)

                                # TODO: check if eval_result is list or not, its true if eval_result is not list

                                raw_str = raw_str.replace(f'`{exp}`', eval_result[0] if isinstance(eval_result,
                                                                                                   list) else eval_result)

                            template[q_type_name][q_property_name][q_property_format_name][i] = raw_str

        free_template_datasets(self.__template['datasets'])
        return Template(template)

    def get_question(self, bool_answer, question_type, format):
        """
        change a template structure to the question structure
        we do it after parsing a template

        :param question_type:
        :param format:
        :return:
        """

        template = self.__template
        question = template[question_type]

        question.update({
            'type': question_type[1:],
            'tags': template['tags'],
            'usage': template['usage'],
            # 'values': template['values'],
            'datasets': template['datasets'],
        })

        for type in question['title']:
            question['title'][type] = choose(
                [t for i, t in enumerate(question['title'][type]) if i % 2 == int(bool_answer)])

        if question['type'] == 'bool':
            question['answer'] = {'text': [str(bool_answer).lower()]}
        
        if 'choice' in question:
            for field in question['choice']:
                question['choice'][field] += question['answer'][field]


        return Question(question)

    def generate_question(self, metadata={}, question_type=None, format={}):

        if self.__problems:
            raise SyntaxError(f'there is some error with the template: {self.__problems}')

        question_type = choose(self.get_question_types()) if question_type is None else f'&{question_type}'
        bool_answer = rand([True, False])

        parsed_template = self.parse(bool_answer, metadata)
        question_object = parsed_template.get_question(bool_answer, question_type, format)

        return question_object

    def add_function(self):

        logger.info('trying to add tempalte to mongo ...')
        template = self.dict()
        template['problems'] = self.problems()
        template['ok'] = True if self.problems() == [] else False
        result = mongo_client.TemplateManager.templates.insert_one(template)

        logger.info(result)

        return result

    def test_function(self):
        log_list = []
        log_list_handler = ListHandler(log_list)
        logger.addHandler(log_list_handler)

        if self.problems():
            logger.info('> There are some error :')
            for problem in template.problems():
                logger.error(problem)

        else:
            logger.info('> parsed template :')
            logger.critical(json.dumps(self.parse().dict(), indent=4, ensure_ascii=False))

            logger.info('> question :')
            logger.critical(json.dumps(self.generate_question().dict(), indent=4, ensure_ascii=False))

        logger.removeHandler(log_list_handler)
        print('log_list', log_list)
        return {'runing_log': log_list, 'template_problems': self.problems}

    def __test_duplication(self):
        return True

    def __test_acceptance(self):
        votes = self.__template['__test_info']['acceptance']['votes']
        return len(votes) >= config.template.min_vote

    def __test_data(self):
        """
        check if necessary databases for this template is exist and save problems in __problems
        """
        template_datasets = self.__template['datasets']

        finded_datasets = list(mongo_client.DataManager.datasets.aggregate([
            {'$match': {'name': {'$in': template_datasets}}},
            {'$project': {'_id': 1, 'name': 1, 'state': 1,
                          'ok': {'$eq': ["$state", 'in_use']}}}
        ]))

        not_finded_datasets = list(set(template_datasets) - set([ds['name'] for ds in finded_datasets]))

        datasets_list = finded_datasets + [{'name': ds, 'state': 'null', 'ok': False} for ds in not_finded_datasets]

        self.__template['__test_info']['data']['datasets'] = datasets_list

        for ds in datasets_list:
            if not ds['ok']:
                return False
        return True

    def __test_structure(self):
        """
        check's the format of template json and save problems in __problems
        """
        test_bool = True
        sections = []
        template_consts = ['usage', 'values', 'datasets', 'time_function',
                           'score_function', 'tags', '__state', '__test_info',
                           '__idea']

        for key in template_consts:
            if key in self.__template:
                sections.append({'name': key, 'ok': True, 'problem':[]})
            else:
                test_bool = False if test_bool else test_bool
                sections.append({'name': key, 'ok': False, 
                                 'problem': [f'template object must have a "{key}" in it']})
                
        question_types = self.get_question_types()
        logger.critical(f"found this question types: {question_types}")

        for q_type in question_types:
            problems = []

            if not (q_type in self.__template_formatter):
                problems.append(f"there is an undefined question type in template: {q_type}")

            for q_prop in self.__template[q_type]:
                if not (q_prop in self.__template_formatter[q_type]):
                    problems.append(f'there is an undefined field in "{q_type}" question in template: {q_prop}')

            q_prop_requires_list = [item for item in
                              set(self.__template_formatter[q_type].keys()) - set(self.__template[q_type].keys())
                              if self.__template_formatter[q_type][item]]

            if q_prop_requires_list:
                problems.append(f"there is no {q_prop_requires_list} in {q_type} question")

            test_bool = problems != [] if test_bool else test_bool
            sections.append({'name': q_type, 'ok': problems != [], 'problem': problems})
        
        pprint(self.__template)
        self.__template['__test_info']['structure']['sections'] = sections
        return test_bool

    def __test_generation(self):
        pass

    def __test_manual(self):
        votes = self.__template['__test_info']['manual']['votes']
        return len(votes) >= config.template.min_vote


    def __test_usage_tagging(self):
        usage_list = self.__template['usage']
        return usage_list != []

from pprint import pprint
def load_data(dataset_name):
    '''
    Loads the given dataset and returns it

    Parameters
    ----------
    dataset_name : str
        name of dataset
    '''
    data = pd.DataFrame()

    for i in range(5):
        try:
            logger.info(f'trying to load {dataset_name} dataset from hard disk...')
            data = pd.DataFrame(json.load(open(f'{config.dir.dataset}/{dataset_name}db.json', encoding='utf-8')))
            logger.info(f'loading {dataset_name} dataset is done.')
            break
        except Exception as error:
            logger.error(f'could not open dataset {dataset_name} from {config.dir.dataset} directory because {error}')

    return data


def load_template_datasets(necesery_datasets):
    logger.debug(f'load: {necesery_datasets}')

    for db in necesery_datasets:
        globals()[db] = load_data(db)

def free_template_datasets(datasets):
    logger.debug(f'free: {datasets}')

    for db in datasets:
        globals().drop(db)