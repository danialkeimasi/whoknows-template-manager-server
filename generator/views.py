from django.http import HttpResponse , JsonResponse
from json import JSONEncoder

import random
import json
import sys
from pprint import pprint

from django.views.decorators.csrf import csrf_exempt
#sys.path.insert(0, 'template_engine')
from template_engine.TemplateEngine import create_question, check_answer ,get_templates_list,template_engine


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def createquestion(request):
	tags = request.GET.get('tags', '').split(',')
	templates_id = request.GET.get('templates', '').split(',')
	subtitle_type = request.GET.get('subtitle_type', '').split(',')
	count = int(request.GET.get('count', 0))
	
	templates = []
	all_templates = get_templates_list(tags)
	
	
	templates = [template for template in all_templates if (not templates_id or 'id' not in template or template['id'] in templates_id) and (not subtitle_type or 'subtitleType' not in template or template['subtitleType'] in subtitle_type)]
	
	
	random.shuffle(templates)
	questions = []
	
	#print(templates)
	
	for i, template in enumerate(templates * 10):
		if len(questions) == count: break
		
		new_question, problems = template_engine(template)
		
		
		if new_question['active']:
			questions += [new_question]
	
	
	"""
	pprint({
		'tags'		: tags,
		'questions'	: questions
	})
	"""
	
	try:
		body = json.dumps({
			'questions': questions
		})
	except:
		body = json.dumps({
			'questions': []
		})
	
	return HttpResponse(body)


@csrf_exempt #for exempt this view not to see it as a form validation
def createtemplate(request): #this view would return a bunch of templates as a json with spesific tag which are given by POST and a status as well

    if 'tags' in request.POST:  tags = request.POST.get('tags','').split(',')
    else:   tags = ['movie',]

    templates = get_templates_list(tags)

    body = {
        'templates' : templates ,
        'status'    : 'ok' ,
    }

    return JsonResponse(body,encoder=JSONEncoder)


@csrf_exempt
def createque(request):
    isValid = True
    if 'tags' in request.POST: tags = request.POST.get('tags' , '').split(',')
    else: isValid = False
    if isValid and 'count' in request.POST: count = request.POST.get('count' , 0).split(',')
    else: count = 1

    if isValid:
        templates = get_templates_list(tags=tags)
        questions = []
        for template in templates:
            questions.append(template_engine(template))
        body = {
            'questions' : questions,
            'status'    : 'ok',
        }
        return JsonResponse(body , encoder=JSONEncoder)
    else : return JsonResponse({'status':'bad'} , encoder=JSONEncoder)


def checkanswer(request): 
	guess 		= request.GET.get('guess', '')
	questionID = request.GET.get('questionID', ''
	
	pprint({
		'guess'			: guess,
		'questionID'	: questionID
	})
	
	score = check_answer(guess, questionID)

	body = {
		'score': score
	}

	pprint(body)

	return HttpResponse(json.dumps(body))
