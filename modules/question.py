import json

from config import SETTINGS
from modules.tools.functions import find_format


class Question:
    """ a simple class for a question

    Args:
        question_dict (dict): the question in a dict.

    Attributes:
        __question (dict): question object as dict
        __problems (list): list of problems
    """
    __question_formatter = json.load(open(SETTINGS.dir.question_formatter))

    def __init__(self, question_dict):
        self.__question = question_dict
        self.__metadata = question_dict['metadata'] if 'metadata' in question_dict else None
        self.__problems = []
        self.test_question()

    def dict(self) -> dict:
        """ get the question as dict

        Returns:
            dict: question object
        """
        return self.__question

    def problems(self) -> list:
        """ question problems

        Returns:
            list: list of templates
        """
        return self.__problems

    def is_ok(self) -> bool:
        """ check if question is ok

        Returns:
            bool: return True if there is no problem with question
        """
        return self.__problems == []

    def test_question(self):
        """ run the question test function again """
        self.__problems = []
        self.__test_structure()

    def raise_if_problems(self):
        if not self.is_ok():
            raise TypeError(f"question error: {self.problems()}")
        return self

    def __test_structure(self) -> bool:
        """ test the structure of template

        Returns:
            bool: return True if there is no structure problems
        """
        question = self.__question
        metadata = self.__metadata
        problems = []

        if 'type' not in question:
            problems.append('there is no "type" field in question')

        question_type = question['type']
        required_section = \
        [section for section in self.__question_formatter[question_type] if self.__question_formatter[question_type][section]]
        not_found_section = list(set(required_section) - set([field['section'] for field in question['fields']]))

        if not_found_section != []:
            problems.append(f'question must have the following sections: {not_found_section}')

        self.__problems += problems
        return problems != []
