import os
import json
import copy
import json
import random
import re
import traceback

import jsonschema
import pandas as pd

from pymongo.cursor import Cursor

from config import logger, mongo_client, SETTINGS
from modules.question import Question
from modules.tools.functions import choose, rand, to_list, traceback_shortener, generate
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
        """ template constractor """
        self.__template = template_dict
        self.__template['problems'] = []

        if not ('__test_info' in self.__template and self.__template['__test_info'] != {}):
            self.__template['__test_info'] = self.__empty_template['__test_info']

    def dict(self) -> dict:
        """ returns question template as a dict object. """
        return self.__template

    def fields_filter(self, key: str, value: str):
        """ filter the fields with key and value """
        return [field for field in self.__template['fields'] if field[key] == value]

    def get_question_types(self) -> list:
        """ get all the question types that can make with the template.

        Returns:
            list: all the question types that we can make.
        """
        return list(set([question_type['question_type'] for question_type in self.__template['fields']]))

    def parse(self, metadata: dict = {}, run_command: str = ''):
        """
        eval the variables in the template with data that we have in datasets,
        and return a new template object that has no variable in sentences.

        Args:
            metadata (dict): needed metadata for parsing template.

        Returns:
            Template: parsed template, replaced every variable with datasets.
        """

        db = mongo_client.datasets
        template = copy.deepcopy(self.__template)

        val = {}
        val.update(metadata)

        for value_dict in template['values']:
            key, value = value_dict['key'], value_dict['content']

            logger.info(f'values["{key}"] is going to eval')
            try:
                eval_result = eval(value)
                eval_result = list(eval_result) if isinstance(eval_result, Cursor) else eval_result

            except Exception as e:
                raise type(e)(f'in the validating values[\'{key}\']: {e}') from e

            else:
                val.update({key: eval_result})

        template['values'] = val

        if run_command:
            return eval(run_command)

        db = None
        reg_str = r'[^`]*?`([^`]*?)`[^`]*?'

        for i, field_dict in enumerate(template['fields']):
            raw_str = str(field_dict['content'])

            if field_dict['type'] == 'generator':

                exp = raw_str
                try:
                    eval_result = eval(exp)
                    if isinstance(eval_result, list):
                        eval_result = list(map(str, eval_result))
                    else:
                        eval_result = str(eval_result)

                except Exception as e:
                    raise type(e)(f"in the validating [{key}][{i}]: `{exp}`: {e}") from e
                else:
                    field_dict.update({'content': eval_result})

            elif field_dict['type'] == 'str':
                while re.search(reg_str, raw_str):
                    exp = re.search(reg_str, raw_str).group(1)
                    try:
                        eval_result = eval(exp)
                    except Exception as e:
                        raise type(e)(f"in the validating [{key}][{i}]: `{exp}`: {e}") from e
                    else:
                        raw_str = raw_str.replace(f'`{exp}`', eval_result[0] if \
                            isinstance(eval_result, list) else str(eval_result))

                field_dict.update({'content': raw_str})

            template['fields'][i] = field_dict

        return Template(template)

    def get_question(self, question_type: str, question_format: str, metadata: dict) -> Question:
        """
        change a template structure to the question structure.
        we do it after parsing a template.


        Args:
            question_type (str): question type that we want.
            question_format (str): format of title and choices. can be text, photo, audio, video.

        Returns:
            Question: generated question.
        """
        template = self.__template
        fields = self.fields_filter('question_type', question_type)

        if question_type == 'bool':
            metadata.update({'NOTC': 1, 'NOFC': 1})
        elif question_type == 'choose':
            metadata.update({'NOTC': 1})
        elif question_type == 'write':
            metadata.update({'NOFC': 0})

        logger.info(f'question_type: {question_type}, metadata: {metadata}')
        logger.debug(f'fields after parse {fields}')

        # handling generators
        final_fields = []

        for field in fields:
            if field['type'] == 'generator':
                for item in field['content']:
                    field_new = field.copy()
                    field_new.update({'type': 'str', 'content': item})

                    final_fields.append(field_new)
            else:
                final_fields.append(field)

        fields = final_fields

        logger.debug(f'fields after expand {final_fields}')

        # handle titles
        fields_without_titles = [field for field in fields if field['section'] != 'title']
        titles = [field for field in fields if field['section'] == 'title']
        fields = fields_without_titles + [random.choice(titles)]

        #handle choices
        fields_without_choice = [field for field in fields if field['section'] != 'choice']
        choices = [field for field in fields if field['section'] == 'choice']
        if choices and question_type != 'write':
            choices_True = random.sample([choice for choice in choices if choice['correct'] == True], metadata['NOTC'])
            choices_False = random.sample([choice for choice in choices if choice['correct'] == False], metadata['NOFC'])

            choices = choices_False + choices_True
            random.shuffle(choices_False + choices_True)

            fields = fields_without_choice + choices

        if question_type == 'bool':
            title = [field for field in fields if field['section'] == 'title'][0]
            fields += [
                {
                    "question_type": "bool",
                    "section": "choice",
                    "format": "text",
                    "type": "str",
                    "content": True,
                    "correct": title['correct']
                },
                {
                    "question_type": "bool",
                    "section": "choice",
                    "format": "text",
                    "type": "str",
                    "content": False,
                    "correct": not title['correct']
                },
            ]

        #handle subtitles
        fields_without_subtitles = [field for field in fields if field['section'] != 'subtitle']
        subtitles = [field for field in fields if field['section'] == 'subtitle']
        if subtitles:
            subtitles = random.sample(subtitles, metadata['NOS'])
            fields = fields_without_subtitles + subtitles

        #generate question
        question = {'fields': fields}
        question['metadata'] = metadata

        question.update({
            'template_id': template['_id'],
            'type': question_type,
            'tags': template['tags'],
            'usage': template['usage'],
            'datasets': template['datasets'],
            'values': template['values'],
        })

        logger.debug(f'question ready {question}')
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

        metadata = self.get_metadata(metadata)

        if self.get_question_types() == []:
            raise ValueError('this template is not have any question type')

        question_type = question_type if question_type else random.choice(self.get_question_types())

        question_object = self.parse(metadata=metadata).get_question(question_type, question_format, metadata)

        return question_object

    def __test_duplication(self) -> bool:
        """ finds duplicate templates that we found in the database.

        Returns:
            bool: test if we have not found duplicate template.

        """
        is_ok = True
        problems = []

        self.__template['__test_info']['duplication'] = {
            'similars': [],
            'problems': problems,
            'ok': is_ok
        }

        for problem in problems:
            self.__template['problems'].append({'test': 'duplication', 'error': problem})

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
        for problem in problems:
            self.__template['problems'].append({'test': 'acceptance', 'error': problem})

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

        not_found_tags = list(set(template_datasets) - set([dataset['headers']['name'] for dataset in found_datasets]))
        datasets_list = found_datasets + \
                        [{'headers': {'name': dataset, 'state': 'null'}, 'ok': False} for dataset in not_found_tags]

        for dataset in datasets_list:
            if not dataset['ok'] and dataset['headers']['state'] == 'null':
                problems.append(f"{dataset['headers']['name']} dataset is not found on datasets! {found_datasets}")
            elif not dataset['ok'] and dataset['headers']['state'] != 'in_use':
                problems.append(f"{dataset['headers']['name']} dataset is not ready to use yet!")
            elif not dataset['ok']:
                problems.append(f"something wrong happend about {dataset['headers']['name']}!")

        is_ok = all([dataset['ok'] for dataset in datasets_list])

        self.__template['__test_info']['data'] = {
            'datasets': datasets_list,
            'problems': problems,
            'ok': is_ok,
        }
        for problem in problems:
            self.__template['problems'].append({'test': 'data', 'error': problem})

        return is_ok


    def __test_tags(self) -> bool:
        """ check if tags is valid for this template.

        Returns:
            bool: return True if we have all tags in valid tags.
        """

        problems = []

        allowed_tags = list(mongo_client.main_server.tags.find())
        allowed_tags = [tag['name'] for tag in allowed_tags] + [tag['persianName'] for tag in allowed_tags]

        tags = []
        for tag in self.__template['tags']:
            tags.append({
                'name': tag,
                'ok': tag in allowed_tags
            })

            if not tag in allowed_tags:
                problems.append(f'this tag is not allowed: {tag}.')

        is_ok = all([tag['ok'] for tag in tags])

        self.__template['__test_info']['tags'] = {
            'tags': tags,
            'problems': problems,
            'ok': is_ok,
        }
        for problem in problems:
            self.__template['problems'].append({'test': 'tags', 'error': problem})

        return is_ok

    def __test_schema(self) -> bool:
        """ schema test for template that proves structure of template.

        Returns:
            bool: return True if template struct is validate by schema.
        """

        try:
            self.__schema_validator.validate(self.__template)

        except Exception:
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
        logger.critical(f"found this question types: {question_types}")

        problems_general = []

        if self.__template['fields'] == []:
            problems_general.append('this template is not have any fields')

        for questuin_type in question_types:
            problems = []

            if not (questuin_type in self.__template_formatter):
                problems.append(f"there is an undefined question type in template: {questuin_type}")

            for question_section in self.fields_filter('question_type', questuin_type):
                if not (question_section['section'] in self.__template_formatter[questuin_type]):
                    problems.append(f'there is an undefined field for "{questuin_type}" question in template: {question_section}')

            question_sections_required = [
                item for item in
                set(self.__template_formatter[questuin_type].keys()) - set(map(lambda a: a['section'], self.fields_filter('question_type', questuin_type)))
                if self.__template_formatter[questuin_type][item]
            ]

            if question_sections_required:
                problems.append(f"there is no {question_sections_required} in {questuin_type} question")

            test_bool = problems == [] if test_bool else test_bool
            sections.append({'name': questuin_type, 'ok': problems == [], 'problems': problems})

        for section in sections:
            problems_general += section['problems'] if 'problems' in section else []

        self.__template['__test_info']['structure'] = {
            'problems': problems_general,
            'sections': sections,
            'ok': test_bool
        }
        for problem in problems_general:
            self.__template['problems'].append({'test': 'structure', 'error': problem})

        return test_bool

    def __test_generation(self, count: int = SETTINGS.generation_count) -> bool:
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
        for _ in range(count):

            try:
                question = self.generate_question()
                question_list.append(question.dict())

                if question.is_ok():
                    success_count += 1
                else:
                    raise TypeError(f"question error: {question.problems()}")

            except Exception:
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

        for problem in problem_set:
            self.__template['problems'].append({'test': 'generation', 'error': problem})

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

        for problem in problems:
            self.__template['problems'].append({'test': 'manual', 'error': problem})

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

        for problem in problems:
            self.__template['problems'].append({'test': 'usage_tagging', 'error': problem})

        return usage_test_bool

    def test_update(self):

        tests = SETTINGS.template.tests
        self.__template['__state'] = SETTINGS.template.states[0]

        for test_name in self.__template['__test_info']:
            self.__template['__test_info'][test_name].update({'ok': False, 'problems': []})

        state_number = 0
        all_test_functions = {}
        for state in SETTINGS.template.states[1:]:

            test_functions = {test: getattr(self, f'_Template__test_{test}')() for test in tests[state]['required'] if test}
            all_test_functions.update(test_functions)
            if all(test_functions.values()):
                state_number += 1
            else:
                break

        self.__template['__last_test'] = all_test_functions
        self.__template['__state'] = SETTINGS.template.states[state_number]

        return self

    @staticmethod
    def get_metadata(metadata: dict) -> dict:
        default_metadata = {
            'NOFC': 3,
            'NOS': 1,
            'NOTC': random.randint(1, 4),
            'level': random.randint(1, 10),
        }

        input_metadata = copy.deepcopy(metadata)
        for found_metadata_name in [d_metadata for d_metadata in default_metadata if d_metadata in metadata]:
            default_metadata.pop(found_metadata_name)

        input_metadata.update(default_metadata)
        return input_metadata
