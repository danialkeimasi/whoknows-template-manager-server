import os
import json
import argparse
from modules.config import logger
from modules.tools import project_checkup, get_templates_list, test_templates
from modules.TemplateEngine import template_engine
from modules.config import CONFIG
import logging
from pprint import pprint


def arg_parse():
    '''
    command line interface
    '''

    parser = argparse.ArgumentParser(description='Process some integers.')

    parser.add_argument(
        '-t', '--test', '--test_templates',
        dest='test', default=None,
        type=str,
        
        help='test the templates and make questions',
    )

    parser.add_argument(
        '-ch', '--checkup',
        dest='checkup', default=False,
        action='store_true',
        help='checkup every necessary part of project to work fine',
    )

    parser.add_argument(
        '-d', '--debug',
        dest='debug', default=False,
        action='store_true',
        help='specify debug flag in template_engine',
    )

    parser.add_argument(
        '-s', '--source',
        dest='source', default=False,
        type=str, nargs='+',
        help='sources of templates to test',
    )

    parser.add_argument(
        '-co', '--count',
        dest='count', default=5,
        type=int,
        help='number of test for each template',
    )

    parser.add_argument(
        '-te', '--templateEngine',
        dest='templateEngine', default=None,
        type=str,
        
        help='run the templateEngine function',
    )

    
    parser.add_argument(
        '-log', '--logger',
        dest='logmode', default=False,
        action='store_true',
        help='get the log mode',
    )

    

    args = parser.parse_args()
    
    if args.logmode:
        logger.level = logging.DEBUG
        

    if args.checkup:
        logger.critical('Checkup results : ')
        logger.critical(json.dumps(project_checkup(), indent=4))
        return True
    
    if args.test and os.path.isfile(args.test):
        template = json.load(open(args.test))
        
        if isinstance(template, list):
            template = template[0]

        types = ['multichoices', 'writing', 'true_false', 'selective']
        
        for typ in types:
            print(f'\n\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= {typ} =-=-=-=-=-=-=-=-=-=-=-=-=-\n')
            question = template_engine(template, QT=typ)
            print('\n')
            pprint(question)
            print('\n')


        # chosen_templates = get_templates_list(numbers=args.test, sources=args.source)
        # test_result = test_templates(chosen_templates, try_count=args.count, debug=args.debug)
        # logger.critical(json.dumps(test_result, indent=4))
        return True
    
    return False
