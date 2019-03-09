import random

def to_list(data):
    '''
    if data is not a list, return it as a list
    '''
    return data if isinstance(data, list) else [data]

def randChoose(li, number):
	print('fff', li)
	randli = li[:]
	random.shuffle(randli)
	return randli[:number]


class DataHelper():
	'''
	Data Manager class for working with datasets and accessing it's data easier
	'''
	exp = []

	def __init__(self, exp=None):
		'''
		constract a DataManager
		'''
		self.exp = exp
	
		if exp and not (isinstance(exp, list) and isinstance(exp[0], str)):
			if not isinstance(exp, list):
				exp = [exp]
			
			# we want to find keys of
			# inner list by this for
			for k in exp[0]:
				if len(exp) == 1:
					setattr(self, k, exp[0][k])
				else:
					setattr(self, k, [exp[i][k] for i in range(len(exp))])
	
		elif isinstance(exp, list) and isinstance(exp[0], str):
			self.exp = exp
			
	
	@property
	def one(self):
		'''
		choose random from a list of DataManagers by len of 1
		
		---
			work same as choose(1)
		
		'''
		return randChoose(self.dmlist, 1)
	
	def choose(self, num):
		'''
		choose random from a list of DataManagers by len of "num"
		'''
		if isinstance(self.exp, list):
			return randChoose(self.exp, num)
		else:
			return DataHelper(randChoose(self.pylist, num))

	@property
	def pylist(self):
		'''
		converts the DataManager object to a python List
		'''
		return self.exp
	
	@property
	def dmlist(self):
		'''
		converts the DataManager object to a dataManager List
		'''
		return [DataHelper([item]) for item in self.exp]

