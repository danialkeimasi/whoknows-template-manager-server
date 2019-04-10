from modules.Tools.Functions import choose


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