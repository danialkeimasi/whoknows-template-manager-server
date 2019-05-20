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

    if args.template:

        template = Template(args.template, debug=True, mode='file')

    if args.function:
        
        logger.debug( f'Running function {args.function}')
        
        if args.function in ['test']:

            if template.problems():

                logger.info('> There are some error :')
                
                for problem in template.problems():

                    logger.error(problem)

            else:

                logger.info('> parsed template :')

                logger.critical(json.dumps(template.parse().dict(), indent=4, ensure_ascii=False))

                logger.info('> question :')

                logger.critical(json.dumps(template.generate_question().dict(), indent=4, ensure_ascii=False))


        elif args.function in ['add']:

            template.add()


        


    # if there is any arg, return True
    if (len(sys.argv) == 1) or (len(sys.argv) == 2 and sys.argv[1] == '-log'):
        return False
    else:
        return True
