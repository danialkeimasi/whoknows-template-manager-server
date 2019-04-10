class TemplateError(Exception):
	'''
	this exception raised for template errors,
	- loading problem
	- not have Title or Answer (that means 
	  we can't make question in that specific situation ...)
	
	'''
	pass

class DataError(Exception):
	'''
	when we don't have neccesery data for 
		making our question.
	
	this exception raises when we have 
		data problem, not template problem.
	

	'''