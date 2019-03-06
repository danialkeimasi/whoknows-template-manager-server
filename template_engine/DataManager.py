class DataManager():
	"""
	Data Manager class for working with datasets and accessing it's data easier
	
	"""

	def __init__(self, exp=None):
		if exp:
			if not isinstance(exp, list):
				exp = [exp]

			for k in exp[0]:
				if len(exp) == 1:
					setattr(self, k, exp[0][k])
				else:
					setattr(self, k, [exp[i][k] for i in range(len(exp))])

			if len(exp) > 1:
				setattr(self, 'list', [DataManager([item]) for item in exp])
		else:
			pass