import random
import os
import re


def rand(needList, count=0, exceptions=[], accept_empty=False):
    """
    Return a list of random numbers in range of [start , ... , end],
    Returns only one number(not list) of count is not given

    Args:
        needList (list, range): a list of items that we want to choose from
        count (int, optional): number of random numbers that is needed. Defaults to 0.
        exceptions (list, optional): list of numbers which is needed to be excluded from range. Defaults to [].
    """

    for item in ['needList', 'exceptions']:
        if (not isinstance(locals()[item], list) and not isinstance(locals()[item], range)):
            raise ValueError(f'wrong type for {item} - you use {type(locals()[item])}')

    if len(needList) == 0 and accept_empty:
        return []

    if len(needList) - len(exceptions) < count:
        raise ValueError(f'you choose {count} from {len(needList) - len(exceptions)}')

    needList = [i for i in needList if i not in exceptions]
    # needList = list(set(needList) - set(exceptions))

    choicesList = random.sample(range(len(needList)), 1 if count == 0 else count)

    resultList = [needList[i] for i in choicesList]
    return resultList[0] if count == 0 else resultList


def choose(items, count=1):
    """
    TODO: i change count default from 0 to 1 that always return list in this function, i dont know what happend to code after this :D
    Return a random sebset of given items with length of count
    as a list(returns only one item if count is None, Not as a list)

    Args:
        items (list): a list of items that we want to choose from
        count (int, optional): number of random numbers that is needed. Defaults to 0.

    Returns:
        list:
    """

    return rand(needList=items, count=count)


def to_list(data):
    """ if data is not a list, return it as a list

    Args:
        data: a not iterable object

    Returns:
        list: given object as list
    """
    return data if isinstance(data, list) else [data]


def traceback_shortener(long_error):
    return long_error
    regex = r'"(.*?)"'

    error_list = [trace.strip() for trace in long_error.strip().split('\n')[1::]]
    short_error = f'Error: {error_list[-1]} => Traceback: ' + ' || '.join(error_list[0:-1])

    while re.search(regex, short_error):
        path = re.search(regex, short_error).group(1)
        short_error = short_error.replace(f'"{path}"', os.path.basename(path))

    return short_error
