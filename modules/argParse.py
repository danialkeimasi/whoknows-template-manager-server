import json
import argparse
from config import logger
from tools import project_checkup, get_templates_list, test_templates


def arg_parse():
    '''
    command line interface
    '''

    parser = argparse.ArgumentParser(description='Process some integers.')

    parser.add_argument('-t', '--test', '--test_templates',
                        dest='test', default=False,
                        type=int, nargs='*',
                        help='test the templates and make questions')

    parser.add_argument('-ch', '--checkup',
                        dest='checkup', default=False,
                        action='store_true',
                        help='checkup every necessary part of project to work fine')

    parser.add_argument('-d', '--debug',
                        dest='debug', default=False,
                        action='store_true',
                        help='specify debug flag in template_engine')

    parser.add_argument('-s', '-source',
                        dest='source', default=False,
                        type=str, nargs='+',
                        help='sources of templates to test')

    parser.add_argument('-co', '-count',
                        dest='count', default=5,
                        type=int,
                        help='number of test for each template')

    args = parser.parse_args()
    
    if args.checkup:
        logger.critical('Checkup results : ')
        logger.critical(json.dumps(project_checkup(), indent=4))
    
    if args.test:
        chosen_templates = get_templates_list(numbers=args.test, sources=args.source)
        test_result = test_templates(chosen_templates, try_count=args.count, debug=args.debug)
        logger.critical(json.dumps(test_result, indent=4))