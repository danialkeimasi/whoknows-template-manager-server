from config.config import logger, config
import json
from pprint import pprint
import re
import pandas as pd
import os
from modules.tools.data_container import DataContainer, db, listSub
import copy
from modules.tools.functions import choose, rand, to_list
from modules.question import Question
import random
from config.config import mongo_client, ListHandler, config


class Template:

    __template_formatter = json.load(open(config.dir.template_formatter))
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
        
        if debug:
            self.__check_json_format()
            self.__check_data()


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
        return [key for key in self.__template.keys() if key.startswith('$')]


    def __check_json_format(self):
        """
        check's the format of template json and save problems in __problems
        :param problems:
        """
        problems = []
        template_consts = ['usage', 'values', 'time_function',
                           'score_function', 'tags', '__state', '__test_info',
                           '__idea', 'datasets']
        
        for item in template_consts:
            if not (item in self.__template):
                problems.append(f'template must have a "{item}" part in it')

        question_types = self.get_question_types()
        logger.critical(f"found this question types: {question_types}")

        for q_type in question_types:
            if not (q_type in self.__template_formatter):
                problems.append(f"there is an undefined question type in template: {q_type}")

            for q_property_name in self.__template[q_type].keys():
                if not (q_property_name in self.__template_formatter[q_type]):
                    problems.append(f'there is an undefined part in "{q_type}" type in template: {q_property_name}')

            q_requirements = [item for item in
                              set(self.__template_formatter[q_type].keys()) - set(self.__template[q_type].keys())
                              if self.__template_formatter[q_type][item]]
            if q_requirements:
                problems.append(f"there is no {q_requirements} in {q_type} type question")

        logger.critical(problems)
        self.__update_problems(problems)


    def __get_required_data_names_from_values(self):
        """
        get's a list of databases names that required for template
        from values part of template
        :return database name:
        """
        data_list = []
        data_regex = r'.*?db\(([a-zA-Z]*).*\).*?'

        for val in self.__template['values'].values():
            val = val.replace(' ', '')

            if re.search(data_regex, val):
                data_list.append(re.search(data_regex, val).group(1))

        return list(set(data_list))


    def __check_data(self):
        """
        check if necessary databases for this template is exist and save problems in __problems
        :param problems:
        """
        problems = []
        datasets = self.__template['datasets']

        for ds_name in datasets:
            if not os.path.isfile(f'{config.dir.dataset}/{ds_name}db.json'):
                problems.append(f'dataset named "{ds_name}" not found in {config.dir.dataset}/ dir.')

        logger.critical(problems)
        self.__update_problems(problems)


    def parse(self, bool_answer=True , metadata={}):
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
            for q_property_name in template[q_type_name].keys():
                for q_property_format_name in template[q_type_name][q_property_name].keys():
                    for i, raw_str in enumerate(template[q_type_name][q_property_name][q_property_format_name]):
                        
                        # if raw_str.startswith('$'):
                        if raw_str[0] == '`' and raw_str[-1] == '`':
                            template[q_type_name][q_property_name][q_property_format_name] = eval(raw_str[1:-1])
                        
                        else:
                            while re.search(reg_str, raw_str):
                                exp = re.search(reg_str, raw_str).group(1)
                                eval_result = eval(exp)
                                # if not isinstance(eval_result, str) or not (isinstance(eval_result, list) and len(eval_result) == 1):
                                #     raise ValueError(f'there is some error with template: {q_type_name}, {q_property_name}, {q_property_format_name}: {eval_result}')

                                raw_str = raw_str.replace(f'`{exp}`', eval_result[0] if isinstance(eval_result, list) else eval_result)

                            template[q_type_name][q_property_name][q_property_format_name][i] = raw_str

        return Template(template)


    def get_question(self, bool_answer, question_type, format):
        """
        change a template structure to the question structure
        we do it after parsing a template

        :param question_type:
        :param format:
        :param problems:
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
            question['title'][type] = choose([t for i,t in enumerate(question['title'][type]) if i % 2 == int(bool_answer)])

        if question['type'] == 'bool':
            question['answer'] = {'text': [str(bool_answer).lower()]}

        return Question(question)


    def generate_question(self, metadata={}, question_type=None, format={}):

        if self.__problems:
            raise SyntaxError(f'there is some error with the template: {self.__problems}')

        question_type = choose(self.get_question_types()) if question_type is None else f'${question_type}'
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
    
    logger.debug(f'{necesery_datasets}')

    for db in necesery_datasets:
        globals()[db] = load_data(db)
