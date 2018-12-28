import pandas as pd
import random
import re
import json
import multiprocessing as mp
import psutil
import os
import logging
import requests
from pymongo import MongoClient
from bson.objectid import ObjectId
from pprint import pprint
import copy
import glob
from time import *
#import finglish
import argparse
import tqdm
import itertools


#from templateTools import *


memuseme	= lambda : int(psutil.Process(os.getpid()).memory_info()[0] / 2. ** 30 * 1024)
cpuuseme	= lambda : psutil.Process(os.getpid()).cpu_percent()
cpuuse		= lambda : psutil.cpu_percent()
memuse		= lambda : psutil.virtual_memory()[2]


questions = []

templates = []


def find_format(data):
	"""
	Finds the format of given text, if it's a link then returns link's format else text
	
	Formats
		image : png, jpg, jpeg, gif
		audio : mp3
		video : mp4

		Examples :
				"http://www.host.com/image.jpg" ---> image
				"http://www.host.com/audio.mp3" ---> audio
	"""

	if not isinstance(data, list):
		data = [data]
	if len(data) == 0:
		return 'none'
	for val in data:
		val = str(val)
		if any([val.lower().find(f) != -1 for f in ['.png', '.jpg', '.jpeg', '.gif']]):
			return 'image'
		if any([val.lower().find(f) != -1 for f in ['.mp3']]):
			return 'audio'
		if any([val.lower().find(f) != -1 for f in ['.mp4']]):
			return 'video'

		return 'text'


def isnumber(value):
	"""
	Checks if value is a number
	"""
	try:
		_ = float(value)
		return True
	except:
		pass

	return False


def islink(value):
	"""
	Checks if value is a url
	"""
	if isinstance(value, str):
		if value.find('http') != -1:
			return True

	return False


def mongo_to_json(list_of_objects):
	"""
	Converts MongoDB's ID objects to str so it can be json serializable
	"""
	if not isinstance(list_of_objects, list):
		list_of_objects = [list_of_objects]

	for obj in list_of_objects:
		for key in obj:
			if str(type(obj[key])) == "<class 'bson.objectid.ObjectId'>":
				obj[key] = str(obj[key])
	return list_of_objects


def all_values(dictionary: dict):
	"""
	Rcurcively returns all values in a nested dict

	Parameters
	----------
	dictionary : dict
		dict item that is needed to be uncompress!!!
	"""

	for value in dictionary.values():
		if isinstance(value, dict):
			yield from all_values(value)
		else:
			yield value


def download(url, local_filename=None):
	"""
	Downloads the given url
	
	Parameters
	----------
	url : str
		file's url to be downloaded
	local_filename : str , optional
		name of file after download (defualt is None which means it's name will be given from end of url)
	"""

	if local_filename is None:
		local_filename = url.split('/')[-1]
	else:
		local_filename += '/' + url.split('/')[-1]

	r = requests.get(url, stream=True)
	with open(local_filename, 'wb') as f:
		for chunk in r.iter_content(chunk_size=1024):
			if chunk:
				f.write(chunk)
				#f.flush() commented by recommendation from J.F.Sebastian
	return local_filename


def add_question_to_mongo(question: dict):
	"""
	Inserts the given question to questions's database in MongoDB
	
	# should send auestion/new request instead of directly adding it to database
	# requests.post('localhost:3000/question/new', json={ 'question': question })
	"""

	mongo.GuessIt.question.insert(question)


def add_template_to_mongo(template: dict):
	"""
	Inserts the given template to templates's database in MongoDB
	
	# should send auestion/new request instead of directly adding it to database
	# requests.post('localhost:3000/question/new', json={ 'question': question })
	"""
	
	mongo.GuessIt.template.insert(template)


def initialization(mode='partial'):
	"""
	Initialize needed variables for making a new question, loads translation dataset

	Parameters
	----------
	mode : str, optional
		full mode is for first time , partial is for start of creating a new question
	"""
	
	logger.info('initializating ...')

	#if mode == 'full':
	#	globals()['datasets'] = [re.search('.*\\\\(.*)db\.json', file_name).group(1) for file_name in glob.glob(f'{db_directory}*.json')]
	#	logger.info(f"all datasets that were found: {', '.join(globals()['datasets'])}")

	for dataset in datasets:
		globals()[dataset] = None
		if mode == 'full':
			globals()[dataset + 'db'] = None

	for var in template_arrays:
		globals()[var] = []

	for var in template_dicts:
		globals()[var] = {}

	if mode == 'full':
		try:
			globals()['translation' + 'db'] = load_data('translation')
		except:
			logger.error(f'could not load translation db')

	logger.info('initialization is done.')


def load_data(dbname):
	"""
	Loads the given dataset and returns it
	
	Parameters
	----------
	dbname : str
		name of dataset
	"""

	"""
	TODO : 
		- get path for loading dataset
		- download dataset from server
	"""

	logger.info(f'def load_data(dbname={dbname})')

	problems = []

	data = pd.DataFrame()

	while True:
		try:
			logger.info(f'trying to load {dbname} dataset from hard disk...')

			data = pd.DataFrame(json.load(open(f'{project_dir}/datasets/{dbname}db.json', encoding='utf-8')))

			logger.info(f'loading {dbname} dataset is done.')

			break

		except Exception as error:

			problems += [f'could not open dataset {dbname} from {project_dir}/datasets/ directory because {error}']

			break

			#logger.info(f'trying to download {dbname} dataset from server...')

			#download(f'{db_url}{dbname}db.json', 'database/')
		except:
			logger.error(f'shit happened while loading {dbname} dataset')

			break


	return data, problems


def used_datasets(template):
	"""
	Returns a list of used datasets in the given template

	Parameters
	----------
	template : dict
		template that it's datasets are needed
	"""
	
	"""
	# BUG : does not find datasets that had been used in middle of code. example : director[(movie.name....)]
	"""

	used_dataset = []
	if 'values' not in template:
		return []

	joint_code = ' '.join(template['values'].values())
	while joint_code.find('db') != -1:
		if re.search('db\(([a-zA-Z]*).*\)', joint_code):
			used_dataset += [re.search('db\(([a-zA-Z]*).*\)', joint_code).group(1)]
		joint_code = joint_code[joint_code.find('db') + 2:]
	return used_dataset


def load_used_datasets(template):
	"""
	Loads used datasets in given template into dataset's global variables

	Parameters
	----------
	template : dict
		template that it's datasets are needed to be loaded
	"""
	problems = []

	if memuseme() > 1300:
		initialization()

	for dataset in [re.search('.*?/([a-zA-Z]*?)db.json', address).group(1) for address in glob.glob(f'{project_dir}/datasets/*.json')]:#used_datasets(template):
		if f'{dataset}db' not in globals() or globals()[f'{dataset}db'] is None:
			globals()[dataset + 'db'], new_problems = load_data(dataset)
			problems += new_problems
	return problems


def excluce_datasets(template, ILMIN=0, ILMAX=1):
	"""
	exclude (remove) some parts of used datasets of given template, based on given level (ILMIN , ILMAX)

	Parameters
	----------
	template : dict
		template that it's datasets needs to be excluded
	ILMIN : int
		minimum of internal level
	ILMAX : int
		maxsimum of internal level	
	"""

	for dataset in used_datasets(template):
		if globals()[dataset] is None:

			try:
				if len(globals()[dataset + 'db'].index)*(ILMAX - ILMIN) > 10:
					   globals()[dataset] = globals()[dataset + 'db'].sort_values('popularity', ascending=False).iloc[int(len(globals()[dataset + 'db'].index)*ILMIN):int(len(globals()[dataset + 'db'].index)*ILMAX)]
				else:
					   globals()[dataset] = globals()[dataset + 'db'].sort_values('popularity', ascending=False)
			except:
				globals()[dataset] = globals()[dataset + 'db']#.iloc[int(len(globals()[dataset + 'db'].index)*ILMIN):int(len(globals()[dataset + 'db'].index)*ILMAX)]

			#globals()[dataset] = globals()[dataset + 'db']
			#globals()[dataset].dropna()



def choose(items, count=None):
	"""
	Return a random sebset of given items with length of count as a list(returns only one item if count is None, Not as a list)

	Parameters
	----------
	template : dict
		template that it's datasets needs to be excluded
	ILMIN : int
		minimum of internal level
	ILMAX : int
		maxsimum of internal level	
	"""
	
	random.shuffle(items)
	if count:
		return items[:count]
	else:
		return items[0]

	return items[random.randint(0, len(items))]

	if not items or not rand(0, len(items) - 1, count, [], False):
		return []



	if count == None:
		selected_indices = rand(0, len(items) - 1, 1, [], False)
	else:
		selected_indices = rand(0, len(items) - 1, count, [], False)

	selected_items = []
	for i in selected_indices:
		selected_items += [items[random.randint(0, len(items))]]

	if count == None:
		selected_items = selected_items[0]

	return selected_items


def make_help(data_name, data, exceptions=[], language='en'):
	"""
	Return helps for question, based on given data_name and language

	Parameters
	----------
	data_name : str
		name of data that we need helps about it
	data : *
		****
	exceptions : list
		****
	language : str
		language of needed helps
	"""

	#print(data_name, data, exceptions, language)

	#data_id = data.id

	chosen_helps = []

	helps = {
		'director': {
			'en': {
				'age'	   : "he/she is {data.age} years old",
				'movies'	: "some of his/her movies are {' , '.join(data.movies)}"
			},
			'fa': {
				'age'	   : "او {data.age} سال دارد",
				'movies'	: "تعدادي از فيلم هاي او عبارتند از : {' , '.join(data.movies)}"
			}
		},
		'actor': {
			'en': {
				'age'	   : "he/she is {data.age} years old",
				'movies'	: "some of his/her movies are {' , '.join(data.movies)}"
			},
			'fa': {
				'age'	   : "او {data.age} سال دارد",
				'movies'	: "تعدادي از فيلم هاي او عبارتند از : {' , '.join(data.movies)}"
			}
		},
		'movie': {
			'en': {
				'release_year'   : "it was released in {int(data.release_year)}",
				'imdb_rate'	  : "it's imdb rate is {data.imdb_rate}",
				'stars'		 : "some of it's casts are {' , '.join(data.stars)}",
				'characters'	: "some of it's characters are {' , '.join(data.characters[:3])}",
				'genres'		: "it' genres are {' , '.join(data.genres)}",
				#'tag_line'		: "`choose(data.tag_line)`"
			},
			'fa': {
				'release_year'   : "اين فيلم در سال {int(data.release_year)} منتشر شد",
				'imdb_rate'	  : "امتياز imdb اين فيلم {data.imdb_rate} است",
				'stars'		 : "تعدادی از بازیگران اين فيلم عبارتند از : {' , '.join(tr(data.stars))}",
				'characters'	: "تعدادي از کاراکتر هاي اين فيلم عبارتند از : {' , '.join(tr(data.characters[:3]))}",
				'genres'		: "اين فيلم در ژانر هاي {' , '.join(tr(data.genres))} قرار می گیرد",
				#'tag_line'		: "`choose(data.tag_line)`"
			}
		}
	}[data_name][language]

	for key in [key for key in helps.keys() if key not in exceptions]:
		try:
			e = eval('f"' + helps[key] + '"')
			chosen_helps += [e]
		except:
			pass

	return chosen_helps


def miss(word, rate=0.2):
	"""
	Gets a word and replace some of it's characters with ? and Returns the new word

	Parameters
	----------
	word : str
		wanted word to be changed
	ratio : float, optional
		ratio = (number of ?) / (number of character) = word.count('?') / len(word)
	"""
	
	raw_word = word.replace(' ', '')
	word = list(word)
	miss_count = int(rate * len(raw_word) + 0.5)
	forbiden_chars = [' ']
	forbiden_chars_index = [i for i, c in enumerate(word) if c in forbiden_chars]
	miss_index = rand(0, len(raw_word), miss_count, forbiden_chars_index)
	new_word = ''.join([i in miss_index and '?' or c for i, c in enumerate(word)])
	return new_word


def mess(word):
	"""
	Gets a word and shuffle it's characters

	Parameters
	----------
	word : str
		wanted word to be changed
	"""
	
	forbiden_chars = [' ']
	letters = [c for c in word if not c in forbiden_chars]
	random.shuffle(letters)
	return letters


def tr(phrases, home='en', target='fa'):
	"""
	Translate given phrase or phrases from home language to target language

	Parameters
	----------
	phrases : list, str, int, float
		phrase or phrases needed to be translated
	home : str
		language of given phrase (default is en: english)
	target : str
		target language of phrase
	"""

	return phrases

	if not isinstance(phrases, list): phrases = [phrases]
	else: return_list = True

	translations = phrases

	global translationdb

	for i, phrase in enumerate(phrases):
		phrase_data = db(translationdb[translationdb.phrase == phrases])

		if phrase_data: translation[i] = phrase_data[0].phrase_persian

		try:
			response = requests.get(f'https://glosbe.com/gapi/translate?from={home}&dest={target}&format=json&phrase={phrase}&pretty=true', timeout=2)
			translation[i] = [item['phrase']['text'] for item in response.json()['tuc']]

		except:
			pass

	return translation if return_list else translation[0]
	#text = finglish.f2p(text)


def to_list(data):
	"""
	Returns data itself if it is a list, otherwise returns a list containing the data

	Parameters
	----------
	data : list, any
		data that is needed to be converted to list
	"""

	return data if isinstance(data, list) else [data]


class DataManager():
	"""
	Data Manager class for working with datasets and accessing it's data easier

	
	"""

	def __init__(self, exp=None):
		if exp:
			for k in exp[0]:
				if len(exp) == 1:
					setattr(self, k, exp[0][k])
				else:
					setattr(self, k, [exp[i][k] for i in range(len(exp))])

			if len(exp) > 1:
				setattr(self, 'list', [DataManager([item]) for item in exp])
		else:
			pass


def db(doc, count=1, return_problems=False):
	"""
	Gets a panada's Dataframe(doc) and randomly choose count number of items from dataframe and returns the data as a list of dicts

	Paarmeters
	----------
	doc : dataframe
		dataframe that we want to choose from
	count : int
		number of items which is needed (default is 1)
	return_problems : bool
		specify whether this function should return the problems or not
	"""

	logger.info(f'def db(doc=doc, count={count})')

	if count == 0:
		return []
	try:
		if reload_question:
			global data_id_count
			data = doc[doc.id == question['data_id'][data_id_count]]
			data_id_count += 1
		else:
			if len(doc.index) < count:
				raise 'not enough data for db to choose'

			data = doc.sample(count)
			#question['data_id'].insert(0, list(data.id)[0])
			#question['data'] += data.to_dict('records')

	except Exception as error:
		logger.error(f'def db => {error}')
		return []

	data = data.to_dict('records')

	logger.info(f'def db => done')
	return data


def rand(start, end, count=1, exceptions=[], save=True, try_count=10000):
	"""
	Return a list of random numbers in range of [start , ... , end], Returns only one number(not list) of count is not given

	Parameters
	----------
	start : int, float
		specify the start of range
	end : int, float
		specify the end of range
	count : int
		number of random numbers that is needed
	exceptions : list
		list of numbers which is needed to be excluded from range
	save : bool

	try_count : int
		maximum number of try for finding random numbers (default is 10000)
		this must not exist -- BAD algorithm
	"""

	logger.info(f'def rand(start={start}, end={end}, count={count}, exceptions={exceptions}, save={save})')

	#global r

	if isinstance(exceptions, str): exceptions = int(exceptions)

	if isinstance(exceptions, int): exceptions = [exceptions]

	start = int(start)
	end = int(end)
	exceptions = list(map(int, exceptions))


	if len(set(range(start, end + 1)) - set(exceptions)) == 0:
		return False

	randoms = []

	for i in range(10000):
		newrand = random.randint(start, end)

		if not newrand in exceptions and not newrand in randoms:
			randoms.append(newrand)

		if len(randoms) == count:
			#if save: r += randoms
			logger.info(f'def rand => done')
			return randoms[0] if count == 1 else randoms

	logger.error(f'def rand => could not find random numbers after {try_count} circle')


def evaluate(text, exp, storage=[], key=None):
	"""
	Get a text and replace expression(exp) part of it with eval(exp)

	Parameters
	----------
	text : str
		str which is neede to be evaluated
	exp : str
		expression part of text
	text : str
		str which is neede to be evaluated
	storege : *
		***
	key : *
		***
	
	"""

	logger.info(f'def evaluate:')

	e = eval(exp)

	if isinstance(e, set):
		e = list(e)

	if key:
		storage[key] = e
		globals()[f'v_{key}'] = e
		setattr(globals()['var'], key, e)
	else:
		if isinstance(e, list):
			storage += e
		else:
			storage += [e]

	if not isinstance(e, list):
		e = [str(e)]
	e = list(map(str, list(e)))

	text = text.replace(f'`{exp}`', str(e), 1)

	logger.info(e)

	return text


def parse(items, storage=[], key=None, mode=''):
	"""
	Gets a list of items and evaluate every code part of it's strings
	Example : 
		['2 + 2 = `2 + 2`', ...] ---> ['2 + 2 = 4', ...]

	Parameters
	----------
	items : list
		items to be parsed
	storege : *
		***
	key : *
		***
	
	"""

	if isinstance(items, str):
		items = [items]

	for i, item in enumerate(items):
		while 1:

			rex = re.search(r'.*?`(.*?)`.*?', items[i])
			if rex:
				exp = rex.group(1)
				items[i] = evaluate(items[i], exp, storage, key)

			else:
				break

	return items


def check_tag_math(template, question={}):
	"""
	Checks if given template should has the 'math' tag
	
	Parameters
	----------
	tempalte : dict
		wanted tmplate to be checked
	question : dict
		***
	"""

	if any(['expression' in title for title in template['titles']]) and \
		any([any([item in title for item in ['+', '*', '-', '/']]) in title for title in template['titles']]):
		return True
	return False


def find_tags(template, question={}):
	"""
	Returns related tags for given template

	Parameters
	----------
	template : dict
		wanted template to be checked
	question : dict
		***
	"""

	tags = ['movie', 'music']

	founded_tags = []
	if 'tags' in template:
		founded_tags += template['tags']

	#founded_tags += [t for t in a + c + s + list(v.values()) if isinstance(t, str) and not isnumber(t) and not islink(t)]
	founded_tags += used_datasets(template)

	for tag in tags:
		if f'check_tag_{tag}' in globals() and globals()[f'check_tag_{tag}'](template, question):
			founded_tags += [tag]

	founded_tags  = list(set(founded_tags))

	return founded_tags


def check_global_constants():
	"""
	Checks conditional values of a question to be right
	"""

	problems = []

	if not 2 <= NOC <= 6:
		problems += ['NOC is wrong!... NOC range is between 2 to 6']

	if not 2 <= NOS <= 6:
		problems += ['NOS is wrong!... NOS range is between 2 to 6']

	if not 0 < ILMAX <= 1:
		problems += ['ILMAX is wrong!... ILMAX range is between 0 to 1']

	if not 0 <= ILMIN < 1:
		problems += ['ILMIN is wrong!... ILMIN range is between 0 to 1']

	if not ILMIN < ILMAX:
		problems += ['ILMIN is bigger than ILMAX!... ILMIN must be smaller than ILMAX']

	return problems


def check_template(template):
	"""
	Checks if a template has all of necessary parts and returns every problem in template if there is any

	Parameters
	----------
	template : dict
		wanted template to be checked
	"""

	problems = []
	if not 'titles' in template:
		problems += ['titles is empty!']

	if not 'answer' in template:
		problems += ['answer is empty!']

	#if not 'choices' in template:
	#	problems += ['choices is empty!']

	return problems


def check_question(question):
	"""
	Checks if a question has all of necessary parts and returns every problem in template if there is any

	Parameters
	----------
	template : dict
		wanted template to be checked
	"""

	problems = []

	if 'choices' in question:
		# check if choices are different from another

		choices = question['choices']
		if len(choices) != len(set(choices)):
			problems += ['there are repetitive choices']

		for choice in choices:
			choice = str(choice)
			if any([choice.find(item) != -1 for item in ['None', 'NaN', 'null']]):
				problems += ['section "choices" has wrong values']

	for section in question:
		for item in setion if isinstance(section, list) else [section]:
			if any([item.find(x) != -1 for x in ['None', 'NaN', 'null']]):
				problems += [f'section "{section}" has wrong values']

	for section in ['title', 'answer']:
		if section not in question:
			problems += [f'section "{section}" is missing']

	for key in question:
		if question[key] in [float('nan')]:
			problems += [f'{key} in values section is empty']

	return problems


def template_engine(template, NOC=3, ILMIN=0, ILMAX=0.1, NOS=4, reload_question=False, data_id=[]):
	"""
	Generate a question with the given template and conditions
	
	Parameter
	---------
	template : dict
		template of question
	NOC : int
		number of choices
	ILMIN : int
		minimum of internal level
	ILMAX : int
		maximum of internal level
	NOS : int
		number of subtitles
	reload_question : bool
		specify whether question should be generated with random data or given data id's (defalst is False)
	data_id : list
		data id's that should be used for reloading question if reload_question is True
	"""
	
	problems = []

	initialization(mode='full')

	globals()['NOC']				= NOC
	globals()['NOS']				= NOS
	globals()['ILMAX']  			= ILMAX
	globals()['ILMIN']  			= ILMIN
	globals()['reload_question']	= reload_question
	globals()['data_id_count']  	= 0
	globals()['question'] 			= {}
	globals()['var']				= DataManager()
	global question
	global var



	question['data'] = []

	if reload_question:
		question['data_id']			= data_id
	else:
		question['data_id']			= []

	if check_template(template) or check_global_constants():
		logger.info(check_template(template) + check_global_constants())
		return

	problems += load_used_datasets(template)
	excluce_datasets(template, ILMIN=ILMIN, ILMAX=ILMAX)

	if debug: logging.info(f'memory usage : all = {memuse()} %  -  me = {memuseme()} MB')

	if '_id' in template:
		question['template']		= str(template['_id'])

	question['number'] = 0
	if 'number' in template:
		question['number']		  	= template['number']

	if 'values' in template:
		for key in template['values']:
			logger.info(f'parsing values ..... *** {key} ***')
			try:
				#parse(template['values'][key], v, key, 'values')
				exp = eval(template['values'][key][1:-1])

				return_type = 'list'
				if not isinstance(exp, list):
					exp = [exp]
					return_type = type(exp)

				if isinstance(exp[0], dict):
					obj = DataManager(exp)
				else:
					obj = exp if return_type == 'list' else exp[0]

				setattr(var, key, obj)


				logger.info(obj)

			except Exception as error:
				problems += [f'there is a problem in parsing values : {key} ..... {error}']


	for section in ['titles', 'titles_fa', 'helps', 'helps_fa']:
		if section in template:
			question[section] = []
			for i, item in enumerate(template[section]):
				if isinstance(item, str) and re.search(r'.*?(`.*?`).*?', item):
					try_count = 5
					while isinstance(item, str) and re.search(r'.*?(`.*?`).*?', item) and try_count:
						try_count -= 1
						try:
							exp = re.search(r'.*?(`.*?`).*?', item).group(1)
							eval_exp = eval(exp[1:-1])
							if item[0] == item[-1] == '`':
								item = eval_exp
							else:
								item = item.replace(exp, str(eval_exp))

						except Exception as error:
							problems += [f'there is a problem in section {section} ... {error}']

					question[section] += to_list(item)
				else:
					question[section] += to_list(item)

	for section in ['choices', 'choices_fa', 'answer', 'answer_fa', 'subtitle', 'subtitle_fa']:
		if section in template:
			question[section] = []
			for item in template[section]:
				try_count = 5
				while isinstance(item, str) and re.search(r'.*?(`.*?`).*?', item) and try_count:
					try_count -= 1
					try:
						exp = re.search(r'.*?`(.*?)`.*?', item).group(1)
						item = eval(exp)
						question[section] += item if isinstance(item, list) else [item]

					except Exception as error:
						problems += [f'there is a problem in section {section} ... {error}']
						break

	for section in ['choices', 'answer', 'subtitle']:
		if section in template and f'{section}_fa' not in template:
			try:
				question[f'{section}_fa'] = [tr(item) for item in question[section]]


			except Exception as error:
				problems += [f'there is a problem in section {section} ... {error}']


	if 'choices' in question:
		question['choices'] += question['answer']

	if 'choices_fa' in question:
		question['choices_fa'] += question['answer_fa']

	question['answer_type'] = find_format(question['answer'])

	if 'subtitle' in question:
		question['subtitle_type'] = find_format(question['subtitle'])
	else:
		question['subtitle_type'] = 'empty'

	question['type'] = template['type']

	question['title'] = random.choice(question['titles'])

	if 'helps' in question and question['helps']:
		random_help_index = random.randint(0, len(question['helps']) - 1)
		question['help'] = question['helps'][random_help_index]

	if 'titles_fa' in question and question['titles_fa']:
		question['title_fa'] = random.choice(question['titles_fa'])

	if 'helps_fa' in question and question['helps_fa']:
		try:
			question['help_fa'] = question['helps_fa'][random_help_index]
		except Exception as error:
			problems += [f'there is a problem in section : helps_fa ..... {error}']


	question['tags']  = find_tags(template, question)

	#if 'usage' not in template:
	#	question['usage'] = ['contest']


	problems += check_question(question)

	if problems:
		question['active'] = False
		question['problems'] = problems
	else:
		question['active'] = True

	return question, problems


def check_answer(guess, questionID):
	"""
	evaluate the score of given 'guess' for question with 'questionID'

	Parameters
	----------
	guess : *
		quess to be evaluated
	questionID : str
		id of question that needs to checked with guess
	"""

	answer = mongo.GuessIt.question.find_one({'_id': ObjectId(questionID)})['answer']
	score = 0
	if answer[0] == guess:
		score = 100

	return score


def create_question(tags, question_count, subtitle_type=['audio', 'video', 'text', 'empty']):
	"""
	Create questions based on given tags and conditions

	Parameters
	----------
	tags : list
		tags of wanted questions
	question_count : int
		number of wanted questions
	subtitle_type : list
		specify valid subtitle_type s for wanted questions
	"""
	
	questions = mongo_to_json(list(mongo.GuessIt.question.find()))
	chosen_questions = []

	for tag in tags:
		chosen_questions += [question for question in questions if tag in question['tags'] and question['subtitle_type'] in subtitle_type]

	if not tag or len(tags) == 0:
		chosen_questions = [question for question in questions]

	random.shuffle(chosen_questions)

	return chosen_questions[:min(question_count, len(chosen_questions))]


def get_templates_list(tags=None):
	"""
	Loads wanted tempaltes from file and return them as a list

	Parameters
	----------
	tags : list
		specifies tags of wanted templates
	"""

	templates = []
	for template_file in glob.glob(f'{project_dir}/generator/template_engine/templates/*.json'):
		new_templates = json.load(open(template_file, encoding="utf-8"))
		for template in new_templates:
			template['source'] = template_file
		templates += new_templates

	if tags is None: return templates

	chosen_templates = []

	for template in templates:
		if any(tag in find_tags(template) for tag in tags):
			chosen_templates += [template]

	"""
	for template in templates:
		if any('tags' in keys for keys in template):
				for tag in tags:
					if tag in template['tags']:
						chosen_templates += [template]
	"""

	return chosen_templates


def test_templates(templates, try_count=5, rounds_count=1, save_result=True):
	"""
	Inspect a template and generate question with it to check it's performance and find it's problems and return the results

	Parameters
	----------
	template : dict
		wanted template to be inspected
	"""

	initialization(mode='full')

	#pprint(template_engine(templates[:][0], reload_question=True,
	#					data_id=['22168547476411738720', '22168547476411738720', '11237477244815026935', '22168547476411738720']))

	questions = []

	templates_test = {}

	for template in tqdm.tqdm(templates):

		templates_test[template['number']] = {
			'problems': []
		}

		logger.info(f"Testing template number : {template['number']}")

		for j in range(try_count):

			question, problems = template_engine(template)

			questions += [question]

			#pprint(question, indent=4)

			if not problems:
				logger.info(f'SUCCESSFULL')

				if use_mongo: add_question_to_mongo(question)


			for problem in problems:

				logger.error(problem)

				templates_test[template['number']]['problems'] += problems

				#test_result['templates'][-1]['problems'] = problems

		if problems: logger.info(f'FAILED')

		json.dump(mongo_to_json(questions), open(f'{project_dir}/generator/template_engine/questions.json', 'w', encoding='utf-8'), indent=4, ensure_ascii=False)



	test_result = {
		'templates_count'	: len(templates),
		'success'			: len(set([question['number'] for question in questions if not question['active']])),
		'fails'				: len(set([question['number'] for question in questions if question['active']])),
		'success_rate'		: str(int(len([True for question in questions if question['active']]) / (len(templates) * try_count) * 100)) + '%',
		'failed_templates'	: sorted(list(set([question['number'] for question in questions if not question['active']]))),
		'templates'			: [{
			'number'		: template['number'],
			'source'		: template['source'],
			'test_count'	: try_count,
			'success'		: len([True for question in questions if question['active'] and question['number'] == template['number']]),
			'fails'			: len([True for question in questions if not question['active'] and question['number'] == template['number']]),
			'success_rate'	: str(int(len([True for question in questions if question['active'] and question['number'] == template['number']]) / (try_count) * 100)) + '%',
			'time_avg'		: 0,
			'problems'		: [problem + f" *** count = {templates_test[template['number']]['problems'].count(problem)}" for problem in list(set(templates_test[template['number']]['problems']))]
		} for template in templates]
		#'problems'		: list(set(all_problems)),

	}

	if save_result:
		json.dump(mongo_to_json(test_result), open(f'{project_dir}/generator/template_engine/test_result.json', 'w+', encoding='utf-8'), indent=4)


	return test_result



datasets = ['movie', 'director', 'song', 'actor', 'footballPlayer', 'footballTeam', 'quote',
			'country', 'book', 'name', 'word', 'volleyballTeam'] #should be done automatically by searching db_directory

debug				= not True
project_dir			= '/root/guessit'
language			= 'fa'
use_mongo			= False

print(re.replace(os.path.realpath(__file__)))

logging.basicConfig(format='### %(asctime)s - %(levelname)-8s : %(message)s \n',
					datefmt='%H:%M:%S',
					level=logging.WARNING,
					handlers=[
						logging.FileHandler(f'{project_dir}/template_engine.log', mode='w+', encoding='utf8', delay=0),
						logging.StreamHandler()
					])

logger = logging.getLogger('TemplateEngine')


if use_mongo: mongo = MongoClient('mongodb://localhost:27017')


if __name__ == '__main__':

	
	parser = argparse.ArgumentParser(description='Process some integers.')

	parser.add_argument('--test', '--test_templates', nargs='*', type=int, dest='test',
		            	default=False, help='test the templates and make questions')

	parser.add_argument('-source', type=str, nargs='+', dest='source', default=False,
		            	help='sources of templates to test')

	parser.add_argument('-count', type=int, default=5, dest='count',
		            	help='number of test for each template')

	args = parser.parse_args()


	if args.test != False:
		chosen_templates = get_templates_list() if len(args.test) == 0 else [template for template in get_templates_list() if template['number'] in args.test]

		if args.source:
			chosen_templates = [chosen_template for chosen_template in chosen_templates if any(chosen_template['source'].find(source) != -1 for source in args.source)]

		test_result = test_templates(chosen_templates, try_count=args.count)

		pprint(test_result)
	else:
		pass
		#test_result = test_templates()
