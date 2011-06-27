'''
Created on Jun 26, 2011

@author: paul
'''

from lib.serializer import Serializer

class StoreManager(Serializer, dict):
    
    def get(self, name):
        '''
        Returns a COPY of the given name. 
        
        Use this when you need a fresh 
        @param name:
        '''
        return self.__getitem__(name).copy()
    
    def add(self, store):
        self.__setitem__(store.name, store)
        

    def pre_save(self):
        for store in self.itervalues():
            if hasattr(store, "pre_save"):
                store.pre_save()
                
    def post_load(self):
        for store in self.itervalues():
            if hasattr(store, "post_load"):
                store.post_load()