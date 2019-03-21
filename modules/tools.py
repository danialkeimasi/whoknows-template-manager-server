import random

def rand(needList, count=0, exceptions=[]):
    '''
	Return a list of random numbers in range of [start , ... , end], Returns only one number(not list) of count is not given
	Parameters
	----------
	needList   : list
        a list of items that we want to choose from
	count      : int
		number of random numbers that is needed
	exceptions : list
		list of numbers which is needed to be excluded from range
	'''
    
    for item in ['needList', 'exceptions']:
        if (not isinstance(locals()[item], list) and not isinstance(locals()[item], range)):
            raise ValueError(f'rand(): wrong type for {item} - you use {type(locals()[item])}')
    
    if len(needList) - len(exceptions) < count:
        raise ValueError(f'rand(): error- you choose {count} from {len(needList) - len(exceptions)}')    
    
    
    needList = list(set(needList) - set(exceptions))

    choicesList = random.sample(range(len(needList)), 1 if count == 0 else count)

    resultList = [needList[i] for i in choicesList]
    return resultList[0] if count == 0 else resultList
    

def choose(items, count=0):
    '''
    Return a random sebset of given items with length of count as a list(returns only one item if count is None, Not as a list)

    Parameters
    ----------
    items : list
        a list of items that we want to choose from
    count : int
        number of random numbers that is needed
    '''
    return rand(needList=items, count=count)

def to_list(data):
    '''
    if data is not a list, return it as a list
    '''
    return data if isinstance(data, list) else [data]