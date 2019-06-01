import json

from config.config import config


class Question:
    """
    a simple class for a question
    """
    __template_formatter = json.load(open(config.dir.template_formatter))

    def __init__(self, question_dict):
        self.__question = question_dict
        self.__problems = []
        self.test_question()

    def dict(self):
        """
        get the question as dict
        :return:
        """
        return self.__question
    
    def problems(self):
        """
        get the problems
        :return:
        """
        return self.__problems

    def is_ok(self):
        """
        check if question is ok
        :return:
        """
        return self.__problems == []

    def test_question(self):
        """
        run the question test function
        :return:
        """
        self.__problems = []
        self.__test_structure()


    def __test_structure(self):
        """
        test the structure of template
        :return:
        """
        question = self.__question
        problems = []

        if 'type' not in question:
            problems += ['there is no "type" field in question']

        q_type = question['type']
        q_field_required = [q_field for q_field in self.__template_formatter[f'&{q_type}'] if self.__template_formatter[f'&{q_type}'][q_field]]
        not_found_field = list(set(q_field_required) - set(question.keys()))

        if not_found_field != []:
            problems += [f'question must have the following fields: {not_found_field}']
        
        self.__problems += problems
        return problems != []
