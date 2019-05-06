from modules.tools.functions import choose
from modules.Tools.Exceptions import *

class DataContainer():
    '''
    Data Manager class for working with datasets and accessing it's data easier
    '''
    exp = []

    def __init__(self, exp=None):
        '''
        constract a DataManager
        '''
        self.exp = exp
        if exp == []:
            # TODO: some error must added
            DataError('DataContainer input is is empty list, some error must happend in data queries')

        else:
            if exp and not (isinstance(exp, list) and isinstance(exp[0], str)):
                if not isinstance(exp, list):
                    exp = [exp]

                # we want to find keys of
                # inner list by this for
                print(len(exp))
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
        '''
        choose random from a list of DataManagers by len of 1

        ---
            work same as choose(1)

        '''
        return choose(self.DClist, 1)

    def choose(self, num):
        '''
        choose random from a list of DataManagers by len of "num"
        '''
        if isinstance(self.exp, list) and not isinstance(self.exp[0], dict):
            return choose(self.exp, num)
        else:
            return DataContainer(choose(self.PYlist, num))

    @property
    def PYlist(self):
        '''
        converts the DataManager object to a python List
        '''
        return self.exp

    @property
    def DClist(self):
        '''
        converts the DataManager object to a dataManager List
        '''
        return [DataContainer([item]) for item in self.exp]
