import json

from config.config import config


class Question:
    __template_formatter = json.load(open(config.dir.template_formatter))

    def __init__(self, question_dict):
        self.__question = question_dict
        self.__problems = []
        self.test_question()

    def dict(self):
        return self.__question
    
    def problems(self):
        return self.__problems

    def is_ok(self):
        return self.__problems != []

    def test_question(self):
        problems = []
        question = self.__question


    def __test_structure(self):
        question = self.__question
        problems = []

        if 'type' not in question:
            problems += ['there is no "type" field in question']

        q_type = question['type']
        q_field_required = [q_field for q_field in self.__template_formatter[f'${q_type}'] if self.__template_formatter[f'${q_type}'][q_field]]
        not_found_field = list(set(q_field_required) - set(question.keys()))

        if not_found_field != []:
            problems += [f'question must have the following fields: {not_found_field}']
        
        self.__problems = problems
        return problems != []
        