import os
import re
import random

from config.config import config


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
    error_list = [trace.strip() for trace in long_error.strip().split('\n')[1::]]
    # return error_list[-1]

    short_error = f'Error: {error_list[-1]} => Traceback: {" || ".join(error_list[0:-1])}'

    regex = r'"(.*?)"'
    while re.search(regex, short_error):
        path = re.search(regex, short_error).group(1)
        short_error = short_error.replace(f'"{path}"', os.path.basename(path))

    return short_error


def find_format(val):
    """
    Finds the format of given data, if it's a link then returns link's format else text

    P-S:
        If data is a list by self (more than one item),
        We know that all of them have same format,
        So, we just find the format of first one.

        Examples :
                "http://www.host.com/image.jpg" ---> image
                "http://www.host.com/audio.mp3" ---> audio
    """

    if any([val.strip().lower().find(f) == len(val) - len(f) for f in config.file_formats.photo]):
        return 'photo'

    if any([val.strip().lower().find(f) == len(val) - len(f) for f in config.file_formats.audio]):
        return 'audio'

    if any([val.strip().lower().find(f) == len(val) - len(f) for f in config.file_formats.video]):
        return 'video'

    return 'text'


def generate(data, count):
    return [choose(data, 0) for i in range(count)]


def map_on_nested_dict(nested_dict: dict, function) -> None:
    """do operation on strings that existed in a nested dictionary

    """
    for key, value in nested_dict.items():
        if isinstance(value, dict):
            map_on_nested_dict(value, function)

        elif isinstance(value, list):
            for i, item in enumerate(value):
                if isinstance(item, str):
                    value[i] = function(item)

        elif isinstance(value, str):
            nested_dict[key] = function(value)
