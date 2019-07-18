import json

from config.config import config


class Question:
    """ a simple class for a question

    Args:
        question_dict (dict): the question in a dict.

    Attributes:
        __question (dict): question object as dict
        __problems (list): list of problems
    """
    __template_formatter = json.load(open(config.dir.template_formatter))

    def __init__(self, question_dict):
        self.__question = question_dict
        self.__metadata = question_dict['metadata'] if 'metadata' in question_dict else None
        self.__problems = []
        self.test_question()

    def dict(self):
        """ get the question as dict

        Returns:
            dict: question object
        """
        return self.__question

    def problems(self):
        """ question problems

        Returns:
            list: list of templates
        """
        return self.__problems

    def is_ok(self):
        """ check if question is ok

        Returns:
            bool: return True if there is no problem with question
        """
        return self.__problems == []

    def test_question(self):
        """ run the question test function again """
        self.__problems = []
        self.__test_structure()


    def __test_structure(self):
        """ test the structure of template

        Returns:
            bool: return True if there is no structure problems
        """
        question = self.__question
        metadata = self.__metadata
        problems = []

        if 'type' not in question:
            problems += ['there is no "type" field in question']

        q_type = question['type']
        q_field_required = [q_field for q_field in self.__template_formatter[f'{config.format.question.exist}{q_type}'] if self.__template_formatter[f'{config.format.question.exist}{q_type}'][q_field]]
        not_found_field = list(set(q_field_required) - set(question.keys()))

        if not_found_field != []:
            problems += [f'question must have the following fields: {not_found_field}']

        if metadata:
            if q_type == 'choose':
                if not('choice' in question):
                    problems += 'there is no choice in question with type of choose'

                lengths = list(set([len(item) for item in question['choice']]) - set([0]))
                if not(len(lengths) == 1 and lengths[0] == metadata['NOC'] + 1):
                    problems += 'there is some problem with choices in the question'

        self.__problems += problems
        return problems != []
