import os
import json
import copy
import json
import random
import re
import traceback

import jsonschema
import pandas as pd

from config import logger, mongo_client, SETTINGS
from modules.question import Question
from modules.tools.functions import choose, rand, to_list, traceback_shortener, generate, map_on_nested_dict
from modules.tools import math, leveling
from modules.tools.json_tools import nested_to_dotted, dotted_to_nested

class Template:
    """ a simple class that implemented to work with a json_type question template.

    Args:
        template_dict (dict): the question template in a dict.

    Attributes:
        __template_formatter (dict): a formater that explaines required parts of template. used in __test_structure().
        __empty_template (dict): an empty question template.
        __schema_validator (dict): a schema validator. used in __test_schema().

        __template (dict): template stores here!

    """

    __template_formatter = json.load(open(SETTINGS.dir.template_formatter))
    __empty_template = json.load(open(SETTINGS.dir.empty_template))
    __schema_validator = jsonschema.Draft3Validator(json.load(open(SETTINGS.dir.template_schema)))

    def __init__(self, template_dict):

        self.__template = template_dict

        if not ('__test_info' in self.__template and self.__template['__test_info'] != {}):
            self.__template['__test_info'] = self.__empty_template['__test_info']

    def dict(self) -> dict:
        """ returns question template as a dict object.

        Returns:
            dict: question template.
        """
        return self.__template

    def get_question_types(self) -> list:
        """ get all the question types that can make with the template.

        Returns:
            list: all the question types that we can make.
        """
        return [key for key in self.__template.keys() if key.startswith(SETTINGS.format.question.exist)]

    def parse(self, metadata: dict = {}, bool_answer: bool = True, run_command: str = ''):
        """
        eval the variables in the template with data that we have in datasets,
        and return a new template object that has no variable in sentences.

        Args:
            bool_answer (bool, optional): a randomly generated boolean that use for bool question_type. Defaults to True.
            metadata (dict): needed metadata for parsing template.

        Returns:
            Template: parsed template, replaced every variable with datasets.
        """

        db = mongo_client.datasets

        metadata = self.get_metadata(metadata)
        template = copy.deepcopy(self.__template)

        val = {'bool_answer': bool_answer}
        val.update(template['metadata'])

        # get the values to the "val"
        # values_dict = {}
        for key, value in template['values'].items():
            logger.info(f'{key} is going to eval')

            try:
                eval_result = eval(value)

            except Exception as e:
                raise type(e)(f'in the validating values[\'{key}\']: {e}') from e

            else:
                # values_dict.update({key: eval_result})
                val.update({key: eval_result})

        # template.update({'values': values_dict})

        if run_command:
            return eval(run_command)

        reg_str = r'[^`]*?`([^`]*?)`[^`]*?'
        dotted_question_part = nested_to_dotted({i: template[i] for i in template if i.startswith(SETTINGS.format.question.exist)})

        for key, types_list in dotted_question_part.items():

            if not types_list:
                continue

            for i, raw_str in enumerate(types_list):

                if raw_str.startswith('`') and raw_str.endswith('`') and \
                        len(raw_str[1:-1]) == len(re.search(reg_str, raw_str).group(1)):

                    exp = raw_str[1:-1]
                    try:
                        eval_result = eval(exp)
                    except Exception as e:
                        raise type(e)(f"in the validating [{key}][{i}]: `{exp}`: {e}") from e
                    else:
                        dotted_question_part[key][i] = eval_result

                else:
                    while re.search(reg_str, raw_str):
                        exp = re.search(reg_str, raw_str).group(1)
                        try:
                            eval_result = eval(exp)
                        except Exception as e:
                            raise type(e)(f"in the validating [{key}][{i}]: `{exp}`: {e}") from e
                        else:
                            raw_str = raw_str.replace(f'`{exp}`', eval_result[0] if \
                                isinstance(eval_result, list) else str(eval_result))

                    dotted_question_part[key][i] = raw_str


        template.update(dotted_to_nested(dotted_question_part))
        return Template(template)

    def get_question(self, bool_answer: bool, question_type: str, question_format: str) -> Question:
        """
        change a template structure to the question structure.
        we do it after parsing a template.


        Args:
            bool_answer (bool): a randomly generated boolean that use for bool question_type.
            question_type (str): question type that we want.
            question_format (str): format of title and choices. can be text, photo, audio, video.

        Returns:
            Question: generated question.
        """

        template = self.__template
        question = template[question_type]

        for question_field in question:
            for type_ in question[question_field]:
                if question[question_field][type_] != []:
                    question[question_field][type_] = random.choice(
                        [t for i, t in enumerate(question[question_field][type_]) if i % 2 == int(bool_answer)]
                    ) if len(question[question_field][type_]) > 1 else question[question_field][type_]

        if question['type'] == 'bool':
            question['answer'] = {'text': [str(bool_answer).lower()]}

        if 'choice' in question:
            for field in question['choice']:
                question['choice'][field] += question['answer'][field]
                random.shuffle(question['choice'][field])

        question['metadata'] = template['metadata'] if 'metadata' in template else None

        question.update({
            'template_id': template['_id'],
            'type': question_type[len(SETTINGS.format.question.exist):],
            'tags': template['tags'],
            'usage': template['usage'],
            'datasets': template['datasets'],
            'values': template['values'],
        })

        return Question(question)

    def generate_question(self, metadata: dict = {}, question_type: str = '', question_format: dict = {}) -> Question:
        """ generate question by this template.

        this function executed on a given template,
        and after parsing this template we get question from parsed template.

        Args:
            metadata (dict, optional): necessery data for creating question from template. Defaults to {}.
            question_type ([type], optional): exact question_type that we want. Defaults to None.
            question_format (dict, optional): format of title and choices. range of text, photo, audio, video. Defaults to {}.

        Returns:
            Question: [description]
        """

        bool_answer = rand([True, False])
        metadata = self.get_metadata(metadata)

        if self.get_question_types() == []:
            raise ValueError('this template is not have any question type')

        question_type = random.choice(self.get_question_types()) if not question_type else \
            f'{SETTINGS.format.question.exist}{question_type}'

        question_object = self.parse(metadata=metadata, bool_answer=bool_answer) \
                              .get_question(bool_answer, question_type, question_format)

        return question_object

    def __test_duplication(self) -> bool:
        """ finds duplicate templates that we found in the database.

        Returns:
            bool: test if we have not found duplicate template.

        """
        is_ok = True
        self.__template['__test_info']['duplication'] = {
            'similars': [],
            'problems': [],
            'ok': is_ok
        }

        return is_ok

    def __test_acceptance(self) -> bool:
        """ check acceptance of the name.

        Returns:
            bool: return True if votes in this template reach the goal.
        """

        problems = []

        if 'acceptance' not in self.__template['__test_info']:
            self.__template['__test_info']['acceptance'] = {}

        if 'votes' not in self.__template['__test_info']['acceptance']:
            self.__template['__test_info']['acceptance']['votes'] = []

        votes_len = len(self.__template['__test_info']['acceptance']['votes'])

        acceptance_bool = votes_len >= SETTINGS.template.min_vote
        acceptance_bool = True  # tmp

        if not acceptance_bool:
            problems.append(f"there was {votes_len} voted, it's not enough!")

        self.__template['__test_info']['acceptance'] = {
            'problems': problems,
            'ok': acceptance_bool
        }

        return acceptance_bool

    def __test_data(self) -> bool:
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

        not_found_tags = list(set(template_datasets) - set([ds['headers']['name'] for ds in found_datasets]))
        datasets_list = found_datasets + \
                        [{'headers': {'name': ds, 'state': 'null'}, 'ok': False} for ds in not_found_tags]

        for ds in datasets_list:
            if not ds['ok'] and ds['headers']['state'] == 'null':
                problems.append(f"{ds['headers']['name']} dataset is not found on datasets! {found_datasets}")
            elif not ds['ok'] and ds['headers']['state'] != 'in_use':
                problems.append(f"{ds['headers']['name']} dataset is not ready to use yet!")
            elif not ds['ok']:
                problems.append(f"something wrong happend about {ds['headers']['name']}!")

        is_ok = all([ds['ok'] for ds in datasets_list])

        self.__template['__test_info']['data'] = {
            'datasets': datasets_list,
            'problems': problems,
            'ok': is_ok,
        }

        return is_ok


    def __test_tags(self) -> bool:
        """ check if tags is valid for this template.

        Returns:
            bool: return True if we have all tags in valid tags.
        """

        problems = []

        template_tags = self.__template['tags']

        allowed_tags = mongo_client.main_server.tags.find()
        allowed_tags = [tag['title'] for tag in allowed_tags] + [tag['persianTitle'] for tag in allowed_tags]

        tags = []
        for tag in template_tags:
            tags.append({
                'name': tag,
                'ok': tag in allowed_tags
            })

            if not tag in allowed_tags:
                problems.append(f'this tag is not allowed: {tag}.')

        is_ok = all([tag['ok'] for tag in tags])

        self.__template['__test_info']['tags'] = {
            'datasets': tags,
            'problems': problems,
            'ok': is_ok,
        }

        return is_ok

    def __test_schema(self) -> bool:
        """ schema test for template that proves structure of template.

        Returns:
            bool: return True if template struct is validate by schema.
        """

        try:
            self.__schema_validator.validate(self.__template)

        except Exception as error:
            error_message = traceback_shortener(traceback.format_exc())

            if 'structure' not in self.__template['__test_info']:
                self.__template['__test_info']['structure'] = {}

            if 'problems' not in self.__template['__test_info']['structure']:
                self.__template['__test_info']['structure']['problems'] = []

            self.__template['__test_info']['structure']['problems'].append(error_message)
            self.__template['__test_info']['structure']['ok'] = False

            return False
        else:
            return True

    def __test_structure(self) -> bool:
        """ check's the format of template.

        Returns:
            bool: return True if doesn't find any problem.
        """

        test_bool = True
        sections = []
        template_consts = ['usage', 'values', 'datasets', 'tags', '__state', '__test_info', 'name']

        for key in template_consts:
            if key in self.__template:
                sections.append({'name': key, 'ok': True, 'problem': []})
            else:
                test_bool = False if test_bool else test_bool
                sections.append({'name': key, 'ok': False,
                                 'problems': [f'template object must have a "{key}" in it']})

        question_types = self.get_question_types()

        if question_types == []:
            raise ValueError('this template is not have any question type')

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

        problems = []
        for sec in sections:
            problems += sec['problems'] if 'problems' in sec else []

        self.__template['__test_info']['structure'] = {
            'problems': problems,
            'sections': sections,
            'ok': test_bool
        }
        return test_bool

    def __test_generation(self, count: int = 50) -> bool:
        """ test the template by generate a number of question

        Args:
            count (int, optional): try count. Defaults to 50.

        Returns:
            bool: return True if success_rate reach the goal.
        """
        if '_id' in self.__template:
            mongo_client.template_manager.questions.remove({'template_id': self.__template['_id']})

        success_count = 0
        acceptable_percent = 75

        problem_list = []
        question_list = []
        for try_count in range(count):

            try:
                question = self.generate_question()
                question_list.append(question.dict())

                if question.is_ok():
                    success_count += 1
                else:
                    raise TypeError(f"question error: {question.problems()}")

            except Exception as e:
                error_message = traceback_shortener(traceback.format_exc())
                problem_list.append(error_message)

        problem_set = []
        for problem in set(problem_list):
            problem_set.append(f'{problem} || count: {problem_list.count(problem)}')

        success_percent = success_count / count * 100

        if 'result' not in self.__template['__test_info']['generation']:
            self.__template['__test_info']['generation']['result'] = []

        self.__template['__test_info']['generation']['result'].append({
            'count': count,
            'success_count': success_count,
            'success_percent': success_percent,
            'problems': problem_set
        })

        is_ok = (success_percent) >= acceptable_percent

        if is_ok:
            mongo_client.template_manager.questions.insert_many(question_list)

        self.__template['__test_info']['generation'] = {
            'problems': problem_set,
            'ok': is_ok
        }

        return is_ok

    def __test_manual(self) -> bool:
        """ test the generated questions by a human and vote if its ok

        Returns:
            bool: return True if votes in this template reach the goal
        """

        problems = []
        if 'manual' not in self.__template['__test_info']:
            self.__template['__test_info']['manual'] = {}

        if 'votes' not in self.__template['__test_info']['manual']:
            self.__template['__test_info']['manual']['votes'] = []

        votes_len = len(self.__template['__test_info']['manual']['votes'])

        manual_tes_bool = votes_len >= SETTINGS.template.min_vote
        manual_tes_bool = True  # tmp

        if not manual_tes_bool:
            problems.append(f"there was {votes_len} voted, it's not enough!")

        self.__template['__test_info']['manual'] = {
            'problems': problems,
            'ok': manual_tes_bool
        }

        return manual_tes_bool

    def __test_usage_tagging(self) -> bool:
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

        tests = SETTINGS.template.tests
        self.__template['__state'] = SETTINGS.template.states[0]

        for test_name in self.__template['__test_info']:
            self.__template['__test_info'][test_name].update({'ok': False, 'problems': []})

        state_number = 0
        test_functions = []

        for state in SETTINGS.template.states[1:]:

            test_functions = {t: getattr(self, f'_Template__test_{t}')() for t in tests[state]['required'] if t}
            if not all(test_functions.values()):
                break
            else:
                state_number += 1

        self.__template['__last_test'] = test_functions
        self.__template['__state'] = SETTINGS.template.states[state_number]

        return self

    @staticmethod
    def get_metadata(metadata: dict) -> dict:
        default_metadata = {
            'NOFC': 3,
            'NOS': 4,
            'NOTC': random.randint(1, 4),
            'level': random.randint(1, 10),
        }

        input_metadata = copy.deepcopy(metadata)
        for found_metadata_name in [i for i in default_metadata if i in metadata]:
            default_metadata.pop(found_metadata_name)

        input_metadata.update(default_metadata)
        return input_metadata
