import argparse
import os
import sys
import json

from pprint import pprint
from modules.template import Template
from config.config import mongo_client, logger



def arg_parse():
    '''
    command line interface
    '''

    parser = argparse.ArgumentParser(description='Process some integers.')
    
    
    parser.add_argument(
        '-r', '--run',
        dest='function', default=None,
        type=str,
        help='name of function to run',
    )

    parser.add_argument(
        '-t', '--template',
        dest='template', default=None,
        type=str,
        help='address of template you wanna work on',
    )
    
    parser.add_argument(
        '-c', '--count',
        dest='count', default=None,
        type=str,
        help='number of iteration',
    )

    parser.add_argument(
        '-d', '--debug',
        dest='debug', default=False,
        action='store_true',
        help='enable debug mode',
    )

    parser.add_argument(
        '-log', '--log_level',
        dest='log_level', default=None,
        type=str,
        help='level of log',
    )

    args = parser.parse_args()


    if args.log_level:
        
        log_levels = ['notset', 'debug', 'info', 'warning', 'error', 'critical']

        logger.setLevel(log_levels.index(args.log_level) * 10 if args.log_level in log_levels else 0)

        '''
            Level 	    Numeric value
            CRITICAL 	50
            ERROR 	    40
            WARNING 	30
            INFO 	    20
            DEBUG 	    10
            NOTSET 	    0
        '''

    if args.function:

        logger.debug( f'runing arg with args.function = {args.function}')
        
        if args.function in ['test']:

            template = Template(json.load(open(args.template)))

            if template.problems():

                logger.info('> There are some error :')
                
                for problem in template.problems():
                    logger.error(problem)

            else:
                logger.info('> parsed template :')
                logger.critical(json.dumps(template.parse().dict(), indent=4))

                logger.info('> question :')
                logger.critical(json.dumps(template.generate_question().dict(), indent=4))


            # chosen_templates = get_templates_list(numbers=args.test, sources=args.source)
            # test_result = test_templates(chosen_templates, try_count=args.count, debug=args.debug)
            # logger.critical(json.dumps(test_result, indent=4))
        
        elif args.function in ['add']:
            dataset.start()
        
        elif args.function in ['test']:
            dataset.start()
        
        elif args.function in ['checkup']:
            dataset.start()
        

    # if there is any arg, return True
    if (len(sys.argv) == 1) or (len(sys.argv) == 2 and sys.argv[1] == '-log'):
        return False
    else:
        return True



    """
    parser.add_argument(
        '-t', '--test', '--test_templates',
        dest='test', default=None,
        type=str,
        help='test the templates and make questions',
    )

    parser.add_argument(
        '-a', '---addTemplate',
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

            template = Template(json.load(open(args.test)))
            if template.problems():
                print('there is some error:')
                pprint(template.problems())
            else:
                print('> parsed template:')
                pprint(template.parse().dict())
                print('> question:')
                pprint(template.generate_question().dict())


            # chosen_templates = get_templates_list(numbers=args.test, sources=args.source)
            # test_result = test_templates(chosen_templates, try_count=args.count, debug=args.debug)
            # logger.critical(json.dumps(test_result, indent=4))
        else:
            raise TemplateError('the given template is not found!')

    if args.addTemplate:
        if os.path.isfile(args.addTemplate):
            template = json.load(open(args.addTemplate))
            template = template[0] if isinstance(template, list) else template
            
            res = mongo_cli
    if args.logmode:
        logger.level = logging.DEBUG
ent.TemplateManager.templates.insert_one(template)
            print(res)
    if args.logmode:
        logger.level = logging.DEBUG

        else:
    if args.logmode:
        logger.level = logging.DEBUG

            raise TemplateE
    if args.logmode:
        logger.level = logging.DEBUG
rror('the given template is not found!')
            
    # if there is any arg, return True
    if (len(sys.argv) == 1) or (len(sys.argv) == 2 and sys.argv[1] =='-log'):
        return False
    else:
        return True

    """