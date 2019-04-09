
class NotEnoughtData(Exception):
	pass

class TemplateTestFailed(Exception):
	pass

class WrongTypeForTemplate(Exception):
	'''
		when you can't generate a question by the template
	'''
	pass

class NoTitle(Exception):
	pass
