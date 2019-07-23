import copy
import json
import os
import traceback
import random
import re

import pandas as pd
import jsonschema

from config.config import logger, mongo_client, ListHandler, config
from modules.question import Question
from modules.tools.data_container import DataContainer, db, listSub
from modules.tools.functions import choose, rand, to_list, traceback_shortener
from bson import json_util
from pprint import pprint


class Template:
    """ a simple class that implemented to work with a json_type question template.

    Args:
        inp (dict): the question template in a dict.
        inp (str): the file address of template.
        mode (str): its specified the "inp" arg and can be 'file_address' or 'dict'.

    Attributes:
        __template_formatter (dict): a formater that explaines required parts of template. used in __test_structure().
        __empty_template (dict): an empty question template.
        __schema_validator (dict): a schema validator. used in __test_schema().

        __template (dict): template stores here!

    """

    __template_formatter = json.load(open(config.dir.template_formatter))
    __empty_template = json.load(open(config.dir.empty_template))
    __schema_validator = jsonschema.Draft3Validator(json.load(open(config.dir.template_schema)))


    def __init__(self, inp, mode='dict'):

        self.__template = json.load(open(inp, encoding='utf8')) if mode == 'file' else \
                          inp                                   if mode == 'dict' else \
                          None

        if not ('__test_info' in self.__template and self.__template['__test_info'] != {}):
            self.__template['__test_info'] = self.__empty_template['__test_info']

    def dict(self):
        """ returns question template as a dict object.

        Returns:
            dict: question template.
        """
        return self.__template

    def get_question_types(self):
        """ get all the question types that can make with the template.

        Returns:
            list: all the question types that we can make.
        """
        return [key for key in self.__template.keys() if key.startswith(config.format.question.exist)]

    def parse(self, metadata, bool_answer=True):
        """
        eval the variables in the template with data that we have in datasets,
        and return a new template object that has no variable in sentences.

        Args:
            bool_answer (bool, optional): a randomly generated boolean that use for bool question_type. Defaults to True.
            metadata (dict): needed metadata for parsing template.

        Returns:
            Template: parsed template, replaced every variable with datasets.
        """
        template = copy.deepcopy(self.__template)

        dbs = load_template_datasets(self.__template['datasets'])
        for key, value in dbs.items():
            locals()[key] = value

        template['metadata'] = metadata

        problems = []
        val = DataContainer()
        setattr(val, 'bool_answer', bool_answer)

        for key, value in metadata.items():
            setattr(val, key, value)

        # get the values to the "val"
        # values_dict = {}
        for key, value in template['values'].items():
            logger.info(f'{key} is going to eval')

            try:
                eval_result = eval(value)
                # values_dict.update({key: eval_result})
                setattr(val, key, eval_result)

            except Exception as e:
                raise type(e)(f'in the validating values[\'{key}\']: {e}') from e

        # template.update({'values': values_dict})

        q_type_names = Template(template).get_question_types()
        reg_str = r'[^`]*?`([^`]*?)`[^`]*?'

        for q_type_name in q_type_names:
            for q_property_name in template[q_type_name]:
                for q_property_format_name in template[q_type_name][q_property_name]:
                    for i, raw_str in enumerate(template[q_type_name][q_property_name][q_property_format_name]):

                        if raw_str.startswith('$'):
                            try:
                                exp = raw_str[1:]
                                template[q_type_name][q_property_name][q_property_format_name] = \
                                    list(map(str, to_list(eval(exp))))

                            except Exception as e:
                                raise type(e)(f"in the validating ['{q_type_name}']['{q_property_name}']"
                                    "['{q_property_format_name}'][{i}]: {raw_str}: {e}") from e

                        else:
                            while re.search(reg_str, raw_str):
                                exp = re.search(reg_str, raw_str).group(1)
                                try:
                                    eval_result = eval(exp)
                                except Exception as e:
                                    raise type(e)(f"in the validating ['{q_type_name}']['{q_property_name}']"
                                        "['{q_property_format_name}'][{i}]: `{exp}`: {e}") from e

                                # TODO: check if eval_result is list or not, its true if eval_result is not list

                                raw_str = raw_str.replace(f'`{exp}`', eval_result[0] if \
                                    isinstance(eval_result, list) else str(eval_result))

                            template[q_type_name][q_property_name][q_property_format_name][i] = raw_str

        # free_template_datasets(self.__template['datasets'])
        return Template(template)

    def get_question(self, bool_answer, question_type, format):
        """
        change a template structure to the question structure.
        we do it after parsing a template.


        Args:
            bool_answer (bool): a randomly generated boolean that use for bool question_type.
            question_type (str): question type that we want.
            format (str): format of title and choices. range of text, photo, audio, video.

        Returns:
            Question: generated question.
        """

        template = self.__template
        question = template[question_type]

        question.update({
            'type': question_type[len(config.format.question.exist):],
            'tags': template['tags'],
            'usage': template['usage'],
            # 'values': template['values'],
            'datasets': template['datasets'],
        })

        for type in question['title']:
            if question['title'][type] != []:
                question['title'][type] = choose(
                    [t for i, t in enumerate(question['title'][type])
                        if i % 2 == int(bool_answer)],
                ) if len(question['title'][type]) > 1 else question['title'][type]

        if question['type'] == 'bool':
            question['answer'] = {'text': [str(bool_answer).lower()]}

        if 'choice' in question:
            for field in question['choice']:
                question['choice'][field] += question['answer'][field]
                random.shuffle(question['choice'][field])

        question['metadata'] = template['metadata'] if 'metadata' in template else None
        return Question(question)

    def generate_question(self, metadata={}, question_type=None, format={}):
        """ generate question by this template.

        this function executed on a given template,
        and after parsing this template we get question from parsed template.

        Args:
            metadata (dict, optional): necessery data for creating question from template. Defaults to {}.
            question_type ([type], optional): exact question_type that we want. Defaults to None.
            format (dict, optional): format of title and choices. range of text, photo, audio, video. Defaults to {}.

        Returns:
            Question: [description]
        """

        default_metadata = {
            'NOC': 3,
            'NOS': 4,
            'NOA': random.randint(1, 4),
            'level': random.randint(1, 10),
        }

        # for found_metadata_name in [i for i in default_metadata if i in metadata]:
        #     default_metadata.pop(found_metadata_name)

        metadata = default_metadata

        question_type = choose(self.get_question_types(), 0) if question_type is None else \
            f'{config.format.question.exist}{question_type}'

        bool_answer = rand([True, False])

        parsed_template = self.parse(metadata=metadata, bool_answer=bool_answer)
        question_object = parsed_template.get_question(bool_answer, question_type, format)

        return question_object

    def __test_duplication(self):
        """ finds duplicate templates that we found in the database.

        Returns:
            bool: test if we have not found duplicate template.

        """
        is_ok = True
        self.__template['__test_info']['duplication'].update({
            'similars': [],
            'problems': [],
            'ok': is_ok
        })

        return is_ok

    def __test_acceptance(self):
        """ check acceptance of the idea.

        Returns:
            bool: return True if votes in this template reach the goal.
        """

        problems = []

        votes_len = len(self.__template['__test_info']['acceptance']['votes'])
        acceptance_bool = votes_len >= config.template.min_vote

        acceptance_bool = True # tmp

        if not acceptance_bool:
            problems.append(f"there was {votes_len} voted, it's not enough!")

        self.__template['__test_info']['acceptance'].update({
            'problems': problems,
            'ok': acceptance_bool
        })

        return acceptance_bool

    def __test_data(self):
        """ check if necessary databases for this template is exist.

        Returns:
            bool: return True if we have all wanted datasets.
        """

        problems = []

        template_datasets = self.__template['datasets']

        found_datasets = list(mongo_client.data_manager.datasets.aggregate([
            {'$match': {'headers.name': {'$in': template_datasets}}},
            {'$project': {'_id': 1, 'headers.name': 1, 'headers.state': 1,
                          'ok': {'$eq': ["$headers.state", 'in_use']}}}
        ]))

        not_found_datasets = list(set(template_datasets) - set([ds['headers']['name'] for ds in found_datasets]))

        datasets_list = found_datasets + \
            [{'headers': {'name': ds, 'state': 'null'}, 'ok': False} for ds in not_found_datasets]

        for ds in datasets_list:
            if not ds['ok'] and ds['headers']['state'] == 'null':
                problems.append(f"{ds['headers']['name']} dataset is not found on datasets! {found_datasets}")
            elif not ds['ok'] and ds['headers']['state'] != 'in_use':
                problems.append(f"{ds['headers']['name']} dataset is not ready to use yet!")
            elif not ds['ok']:
                problems.append(f"something wrong happend about {ds['headers']['name']}!")

        is_ok = all([ds['ok'] for ds in datasets_list])

        self.__template['__test_info']['data'].update({
            'datasets': datasets_list,
            'problems': problems,
            'ok': is_ok,
        })

        return is_ok

    def __test_schema(self):
        """ schema test for template that proves structure of template.

        Returns:
            bool: return True if template struct is validate by schema.
        """

        try:
            self.__schema_validator.validate(self.__template)
            return True

        except Exception as error:

            error_message = traceback_shortener(traceback.format_exc())

            self.__template['__test_info']['structure']['problems'].append(error_message)
            self.__template['__test_info']['structure']['ok'] = False

            return False


    def __test_structure(self):
        """ check's the format of template.

        Returns:
            bool: return True if doesn't find any problem.
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


        self.__template['__test_info']['structure'].update({
            'problems': problems,
            'sections':sections,
            'ok': test_bool
        })
        return test_bool

    def __test_generation(self, count = 50):
        """ test the template by generate a number of question

        Args:
            count (int, optional): try count. Defaults to 50.

        Returns:
            bool: return True if success_rate reach the goal.
        """


        success_count = 0
        acceptable_percent = 75

        problem_list = []
        for try_count in range(count):

            try:
                ques = self.generate_question()
                if ques.is_ok():
                    success_count += 1
                else:
                    raise TypeError(f"question error: {ques.problems()}")

            except Exception as e:
                error_message = traceback_shortener(traceback.format_exc())
                problem_list.append(error_message)

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

        is_ok = (success_percent) >= acceptable_percent

        self.__template['__test_info']['generation'].update({
            'problems': problem_set,
            'ok': is_ok
        })

        return is_ok


    def __test_manual(self):
        """ test the generated questions by a human and vote if its ok

        Returns:
            bool: return True if votes in this template reach the goal
        """

        problems = []

        votes_len = len(self.__template['__test_info']['manual']['votes'])
        manual_tes_bool = votes_len >= config.template.min_vote

        if not manual_tes_bool:
            problems.append(f"there was {votes_len} voted, it's not enough!")

        self.__template['__test_info']['manual'].update({
            'problems': problems,
            'ok': manual_tes_bool
        })

        return manual_tes_bool


    def __test_usage_tagging(self):
        problems = []

        usage_list = self.__template['usage']
        usage_test_bool = usage_list != []

        if not usage_test_bool:
            problems.append(f'the template is not have usage tag')

        self.__template['__test_info']['usage_tagging'].update({
            'problems': problems,
            'ok': usage_test_bool
        })

        return usage_test_bool


    def test_update(self):

        tests = config.template.tests
        self.__template['__state'] = config.template.states[0]

        for test_name in self.__template['__test_info']:
            self.__template['__test_info'][test_name].update({'ok': False})

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

    """ Load one dataset and returns it

    Args:
        dataset_name (str): name of dataset

    Returns:
        pd.DataFrame: the given dataset as a pandas data frame
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
    """ load the datasets that given one by one.

    Args:
        necesery_datasets (list): dataset list.

    Returns:
        list: list of pandas dataFrames
    """

    logger.debug(f'load: {necesery_datasets}')

    dbs = {}
    for db in necesery_datasets:
        dbs[db] = load_data(db)

    return dbs


def free_template_datasets(datasets):
    """ free the datasts from ram

    Args:
        datasets (list): dataset list.
    """

    logger.debug(f'free: {datasets}')

    for db in datasets:
        globals().pop(db)
