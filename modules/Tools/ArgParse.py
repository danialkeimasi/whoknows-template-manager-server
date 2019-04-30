import os
import sys
import json
import argparse
import logging
from pprint import pprint

from modules.Tools.Exceptions import *
from modules.Config import logger, CONFIG
from modules.Tools.Functions import project_checkup, get_templates_list, test_templates
from modules.TemplateEngine import testTemplate_ByCreate_Question
from modules.Tools.TemplateManager import add_template_to_server


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
        '-at', '---addTemplate',
        dest='addTemplate', default=None,
        type=str,

        help='add the template to the templates database',
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

    if args.test:
        if os.path.isfile(args.test):
            template = json.load(open(args.test))
            template = template[0] if isinstance(template, list) else template

            testTemplate_ByCreate_Question(template)

            # chosen_templates = get_templates_list(numbers=args.test, sources=args.source)
            # test_result = test_templates(chosen_templates, try_count=args.count, debug=args.debug)
            # logger.critical(json.dumps(test_result, indent=4))
        else:
            raise TemplateError('the given template is not found!')

    if args.addTemplate:
        if os.path.isfile(args.addTemplate):
            template = json.load(open(args.addTemplate))
            template = template[0] if isinstance(template, list) else template

            add_template_to_server(template)

        else:
            raise TemplateError('the given template is not found!')
            
    # if there is any arg, return True
    if (len(sys.argv) == 1) or (len(sys.argv) == 2 and sys.argv[1] =='-log'):
        return False
    else:
        return True
