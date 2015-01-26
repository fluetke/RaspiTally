'''
Created on 25.01.2015

@author: Florian
'''

class TallyState(enumerate):
    '''
    This enum contains all states a TallyDevice can be in,
    it should be used to keep the states consistent throughout the 3 different apps
    '''

    def __init__(self, params):
        '''
        Constructor
        '''