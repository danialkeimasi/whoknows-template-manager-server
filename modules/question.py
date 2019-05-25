class Question:

    def __init__(self, question_dict = None):
        self.__question = question_dict

    def update_by_dict(self, question_dict):
        self.__question = question_dict

    def dict(self):
        return self.__question

    def check_question(self):
        problems = []
        question = self.__question
        
        
        return problems
