import json
import argparse
from modules.config import logger
from modules.tools import project_checkup, get_templates_list, test_templates
from modules.TemplateEngine import template_engine
from modules.config import CONFIG

from pprint import pprint


def arg_parse():
    '''
    command line interface
    '''

    parser = argparse.ArgumentParser(description='Process some integers.')

    parser.add_argument(
        '-t', '--test', '--test_templates',
        dest='test', default=False,
        type=int, nargs='*',
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
        '-s', '-source',
        dest='source', default=False,
        type=str, nargs='+',
        help='sources of templates to test',
    )

    parser.add_argument(
        '-co', '-count',
        dest='count', default=5,
        type=int,
        help='number of test for each template',
    )

    parser.add_argument(
        '-te', '-templateEngine',
        dest='templateEngine', default=False,
        action='store_true',
        help='run the templateEngine function',
    )

    args = parser.parse_args()
    
    if args.checkup:
        logger.critical('Checkup results : ')
        logger.critical(json.dumps(project_checkup(), indent=4))
        return True
    
    if args.test:
        chosen_templates = get_templates_list(numbers=args.test, sources=args.source)
        test_result = test_templates(chosen_templates, try_count=args.count, debug=args.debug)
        logger.critical(json.dumps(test_result, indent=4))
        return True
    
    if args.templateEngine:
        qaleb = [x for x in json.load(open(f'{CONFIG.templates_dir}/footballTeam,league.json'))if x['__number']==1][0]

        print('\n---\n@input_Template:')
        pprint(qaleb)

        print('\n---\n@funcRun:')

        types = ['multichoices', 'writing', 'true_false', 'selective']
        
        out = [template_engine(qaleb, QT=typ) for typ in types]
        # out = template_engine(qaleb, QT=types[0])
        # out = create_question('footballTeam', 1)
        
        print('\n---\n@output:')
        pprint(out)
        return True
    
    else:
        return False
