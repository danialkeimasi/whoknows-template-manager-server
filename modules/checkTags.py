def check_tag_math(template, question={}):
	"""
	Checks if given template should has the 'math' tag
	
	Parameters
	----------
	tempalte : dict
		wanted template to be checked
	question : dict
		***
	"""

	if any(['expression' in title for title in template['titles']]) and \
		any([any([item in title for item in ['+', '*', '-', '/']]) in title for title in template['titles']]):
		return True
	else:	
		return False
