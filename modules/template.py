import copy
import json
import os
import random
import re

import pandas as pd
import jsonschema

from config.config import logger, mongo_client, ListHandler, config
from modules.question import Question
from modules.tools.data_container import DataContainer, db, listSub
from modules.tools.functions import choose, rand, to_list
from bson import json_util
from pprint import pprint


class Template:
    """
    a class for template
    """
    __template_formatter = json.load(open(config.dir.template_formatter))
    __empty_template = json.load(open(config.dir.empty_template))
    __schema_validator = jsonschema.Draft3Validator(json.load(open(config.dir.template_schema)))

    __default_metadata = {
        'NOC': 3,
        'NOS': 4,
        'NOA': 2,
        'level': 1,
    }

    def __init__(self, inp, debug=False, mode='dict'):
        """
        check template structure if debug is true

        :param inp: dict | file_address
        :param debug: bool
        :param mode:
        """
        self.__template = json.load(open(inp, encoding='utf8')) if mode == 'file' else \
            inp if mode == 'dict' else \
                None

        self.__problems = []
        if not ('__test_info' in self.__template and self.__template['__test_info'] != {}):
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

        dbs = load_template_datasets(self.__template['datasets'])
        for key, value in dbs.items():
            locals()[key] = value


        self.__default_metadata['NOA'] = random.randint(0, 4)
        self.__default_metadata['level'] = random.randint(1, 11)

        for not_found_metadata_name in set(self.__default_metadata.keys()) - set(metadata.keys()):
            metadata[not_found_metadata_name] = self.__default_metadata[not_found_metadata_name]

        problems = []
        val = DataContainer()
        setattr(val, 'bool_answer', bool_answer)

        for key, value in metadata.items():
            setattr(val, key, value)

        # get the values to the "val"
        values_dict = {}
        for key, value in self.__template['values'].items():
            logger.info(f'{key} is going to eval')
            eval_result = eval(value)

            values_dict.update({key: eval_result})
            setattr(val, key, eval_result)

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

        # free_template_datasets(self.__template['datasets'])
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
        """
        generate question by this template
        :param metadata:
        :param question_type:
        :param format:
        :return:
        """
        if self.__problems:
            raise SyntaxError(f'there is some error with the template: {self.__problems}')

        question_type = choose(self.get_question_types()) if question_type is None else f'&{question_type}'
        bool_answer = rand([True, False])

        parsed_template = self.parse(bool_answer, metadata)
        question_object = parsed_template.get_question(bool_answer, question_type, format)

        return question_object

    def add_function(self):
        """
        you can insert this template to the mongodb by this function
        :return:
        TODO: must deleted
        """

        logger.info('trying to add tempalte to mongo ...')
        template = self.dict()
        template['problems'] = self.problems()
        template['ok'] = True if self.problems() == [] else False
        result = mongo_client.TemplateManager.templates.insert_one(template)

        logger.info(result)

        return result

    def test_function(self):
        """
        test the template
        :return:
        """
        template = self.__template
        log_list = []
        log_list_handler = ListHandler(log_list)
        logger.addHandler(log_list_handler)

        if self.problems():
            logger.info('> There are some error :')
            for problem in template.problems():
                logger.error(problem)

        else:
            logger.info('> parsed template :')
            logger.critical(json_util.dumps(self.parse().dict(), indent=4, ensure_ascii=False))

            logger.info('> question :')
            logger.critical(json_util.dumps(self.generate_question().dict(), indent=4, ensure_ascii=False))


        logger.removeHandler(log_list_handler)
        return {'runing_log': log_list, 'template_problems': self.problems}

    def __test_duplication(self):
        """
        return duplicate templates that we found in the database
        :return:
        """

        self.__template['__test_info']['duplication']['similars'] = []
        self.__template['__test_info']['duplication']['problems'] = []
        return True

    def __test_acceptance(self):
        """
        return True if votes in this template reach the goal
        :return:
        """
        problems = []

        votes_len = len(self.__template['__test_info']['acceptance']['votes'])
        acceptance_bool = votes_len >= config.template.min_vote
        
        if not acceptance_bool:
            problems.append(f"there was {votes_len} voted, it's not enough!")
        
        self.__template['__test_info']['acceptance']['problems'] = problems
        return acceptance_bool

    def __test_data(self):
        """
        check if necessary databases for this template is exist and save problems in __problems
        :return:
        """
        problems = []

        template_datasets = self.__template['datasets']

        finded_datasets = list(mongo_client.DataManager.datasets.aggregate([
            {'$match': {'name': {'$in': template_datasets}}},
            {'$project': {'_id': 1, 'name': 1, 'state': 1,
                          'ok': {'$eq': ["$state", 'in_use']}}}
        ]))

        not_finded_datasets = list(set(template_datasets) - set([ds['name'] for ds in finded_datasets]))

        datasets_list = finded_datasets + [{'name': ds, 'state': 'null', 'ok': False} for ds in not_finded_datasets]

        for ds in datasets_list:
            if not ds['ok'] and ds['state'] == 'null':
                problems.append(f"{ds['name']} dataset is not found on datasets!")
            if not ds['ok'] and ds['state'] != 'in_use':
                problems.append(f"{ds['name']} dataset is not ready to use yet!")
            if not ds['ok']:
                problems.append(f"something wrong happend about {ds['name']}!")
        
        self.__template['__test_info']['data']['datasets'] = datasets_list
        self.__template['__test_info']['data']['problems'] = problems

        for ds in datasets_list:
            if not ds['ok']:
                return False
        return True

    def __test_schema(self):
        try:
            self.__schema_validator.validate(self.__template)
            return True
            
        except Exception as e:
            self.__template['__test_info']['structure']['problems'].append(str(e))
            return False
            

    def __test_structure(self):
        """
        check's the format of template json and save problems in __problems
        :return:
        """
        test_bool = True
        sections = []
        template_consts = ['usage', 'values', 'datasets',  'tags', '__state', '__test_info', '__idea']

        for key in template_consts:
            if key in self.__template:
                sections.append({'name': key, 'ok': True, 'problem':[]})
            else:
                test_bool = False if test_bool else test_bool
                sections.append({'name': key, 'ok': False, 
                                 'problems': [f'template object must have a "{key}" in it']})
                
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

            test_bool = problems == [] if test_bool else test_bool
            sections.append({'name': q_type, 'ok': problems == [], 'problems': problems})
        
        prolems = []
        for sec in sections:
            problems += sec['problems'] if 'problems' in sec else []
        
        self.__template['__test_info']['structure']['problems'] = problems
        self.__template['__test_info']['structure']['sections'] = sections
        return test_bool

    def __test_generation(self):
        """
            test the template by generate a number of question
        :return:
        """
        count = 50
        success_count = 0
        acceptable_percent = 75

        problem_list = []
        for try_count in range(count):
            try:
                ques = self.generate_question()
                if ques.is_ok():
                    success_count += 1
            except Exception as e:
                problem_list.append(str(e))
        
        problem_set = []
        for problem in set(problem_list):
            problem_set.append(f'{problem} || count: {problem_list.count(problem)}')

        success_percent = success_count / count * 100

        self.__template['__test_info']['generation']['result'].append({
            'count': count,
            'success_count': success_count,
            'success_percent': success_percent,
            'problems': problem_set
        })

        self.__template['__test_info']['generation']['problems'] = problem_set
        return (success_percent) >= acceptable_percent


    def __test_manual(self):
        """
        return True if votes in this template reach the goal
        :return:
        """
        problems = []

        votes_len = len(self.__template['__test_info']['manual']['votes'])
        manual_tes_bool = votes_len >= config.template.min_vote

        if not manual_tes_bool:
            problems.append(f"there was {votes_len} voted, it's not enough!")

        self.__template['__test_info']['manual']['problems'] = problems
        return manual_tes_bool


    def __test_usage_tagging(self):
        problems = []
        
        usage_list = self.__template['usage']
        usage_test_bool = usage_list != []
        
        if not usage_test_bool:
            problems.append(f'the template is not have usage tag')
        
        self.__template['__test_info']['usage_tagging']['problems'] = problems
        return usage_test_bool


    def test_update(self):
        tests = config.template.tests
        self.__template['__state'] = config.template.states[0]

        state_number = 0
        test_functions = []
        
        for state in config.template.states[1:]:
            test_functions = { t: getattr(self, f'_Template__test_{t}')() for t in tests[state]['required'] if t}
            if not all(test_functions.values()):
                break
            else:
                state_number += 1
        self.__template['__last_test'] = test_functions
        self.__template['__state'] = config.template.states[state_number]

        return self


def load_data(dataset_name):
    """
    Loads the given dataset and returns it

    Parameters
    ----------
    dataset_name : str
        name of dataset
    """
    data = pd.DataFrame()

    for try_count in range(5):
        try:
            logger.info(f'trying to load {dataset_name} dataset from hard disk...')
            data = pd.DataFrame(json.load(open(f'{config.dir.dataset}/{dataset_name}db.json', encoding='utf-8')))
            logger.info(f'loading {dataset_name} dataset is done.')
            break
        except Exception as error:
            logger.error(f'could not open dataset {dataset_name} from {config.dir.dataset} directory because {error}')

    return data


def load_template_datasets(necesery_datasets):
    """
    load the datasets that given to the ram
    :param necesery_datasets:
    :return:
    """
    logger.debug(f'load: {necesery_datasets}')

    dbs = {}
    for db in necesery_datasets:
        dbs[db] = load_data(db)

    return dbs


def free_template_datasets(datasets):
    """
    free the datasts from ram
    :param datasets:
    :return:
    """
    logger.debug(f'free: {datasets}')

    for db in datasets:
        globals().pop(db)
