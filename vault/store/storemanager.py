'''
Created on Jun 26, 2011

@author: paul
'''

from lib.serializer import Serializer

class StoreManagerX(Serializer, dict):
    
    def get(self, name):
        '''
        Returns a COPY of the given name. 
        
        Use this when you need a fresh 
        @param name:
        '''
        return self.__getitem__(name).copy()
    
    def add(self, store):
        self.__setitem__(store.name, store)
        

