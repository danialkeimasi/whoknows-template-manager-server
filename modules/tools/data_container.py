from collections.abc import Iterable

from config.config import logger
from modules.tools.functions import choose


class DataContainer():
    """ Data Manager class for working with datasets and accessing it's data easier

    we just use setattr for adding data to the data to the object

    Raises:
        ValueError: if DataContainer input is is empty list

    Args:
        exp (): data that you want to use as attribute later

    """
    exp = []

    def __init__(self, exp=None):
        """
        constract a DataManager
        """
        self.exp = exp
        if exp == []:
            # TODO: some error must added
            raise ValueError('DataContainer input is is empty list, some error must happend in data queries')

        else:
            if exp and not (isinstance(exp, list) and isinstance(exp[0], str)):
                if not isinstance(exp, list):
                    exp = [exp]

                # we want to find keys of
                # inner list by this for
                for k in exp[0]:
                    if len(exp) == 1:
                        setattr(self, k, exp[0][k])
                    else:
                        Li = []
                        for i in range(len(exp)):
                            Li.append(exp[i][k])
                        setattr(self, k, Li)

            elif isinstance(exp, list) and isinstance(exp[0], str):
                self.exp = exp

    def one(self):
        """ choose random from a list of DataManagers by len of 1


        Returns:
            an element of the given list
        """
        return choose(self.DClist)

    def choose(self, num):
        """ choose random from a list of DataManagers by len of "num"

        Args:
            num (int): how many item you want to choose

        Returns:
            a list of randomly selected elements
        """

        if isinstance(self.exp, list) and not isinstance(self.exp[0], dict):
            return choose(self.exp, num)
        else:
            return DataContainer(choose(self.PYlist, num))

    @property
    def PYlist(self):
        """ converts the DataManager object to a python List

        Returns:
            list: python list of the given data
        """
        return self.exp

    @property
    def DClist(self):
        """ converts the DataContainer object to a DataContainer List

        Returns:
            DataContainer: DataContainer object of the given data
        """
        return [DataContainer([item]) for item in self.exp]


def db(doc, count=0):
    """
    Gets a panada's Dataframe(doc) and randomly choose count number of items
    from dataframe and returns the data as a list of dicts

    Args:
        doc (dataframe): dataframe that we want to choose from
        count (int, optional): number of items which is needed (default is 1). Defaults to 0.

    Raises:
        ValueError: if not enough data for db function to choose from

    Returns:
        DataContainer: loaded data
    """

    try:
        if len(doc.index) < (count if count != 0 else 1):
            logger.info(f'not enough data for db function to choose from, len(doc)={len(doc)} < count={count}')
            raise ValueError(f'not enough data for db function to choose from, len(doc)={len(doc)} < count={count}')

        data = doc.sample(count if count != 0 else 1)

    except Exception as error:
        logger.error(f'{error}')
        return DataContainer([])

    data = data.to_dict('records')
    logger.info(f'done')
    return_data = data[0] if count == 0 else data

    logger.debug(f'db loaded this:' + str(data[0] if count == 0 else data[:5]))
    return DataContainer(return_data)


def listSub(data1, data2):
    """ subtract set for two list

    Args:
        data1 (list): left operand
        data2 (list): right operand

    Returns:
        list: result of set subtract
    """
    data1 = list(data1) if isinstance(data1, Iterable) and not isinstance(data1, str) else [data1]
    data2 = list(data2) if isinstance(data2, Iterable) and not isinstance(data2, str) else [data2]

    logger.debug(f'listSub: {data1[:5]} - {data2[:5]}')
    subedList = [item for item in data1 if not item in data2]

    return DataContainer(subedList)
