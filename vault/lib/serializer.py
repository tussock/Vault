# -*- coding: utf-8 -*-
'''
Created on Apr 23, 2011

@author: paul
'''
import sys
import json

#    Base class of all serializable objects.
class Serializer(object):
    def to_json(self):
        if hasattr(self, "_persistent"):
            #    _persistent lists fields to be saved
            d = {}
            for name in self._persistent:
                d[name] = self.__dict__[name]
        #    lets figure out how to save it...
        elif isinstance(self, dict):
            d = self
        #    TODO! Should do all the other types here... 
        else:  
            #    Otherwise we do all fields, but *not* fields
            #    starting with "_"
            d = {}
            for name in self.__dict__:
                if name[0] != "_":
                    value = self.__dict__[name]
                    if hasattr(value, "to_json"):
                        value = value.to_json()
                    d[name] = value
            
        return {'__class__': self.__class__.__name__,
                '__module__': self.__class__.__module__,
                '__value__': d}
    @classmethod        
    def from_json(cls, d):
        obj = cls()
        obj.__dict__ = d["__value__"]
        return obj
    
     
        
        
def to_json(obj):
    if hasattr(obj, "to_json"):
        return obj.to_json()
    raise TypeError(repr(obj) + ' is not JSON serializable')

def from_json(obj):
    if '__class__' in obj:               
        classname = obj["__class__"]
        modulename = obj["__module__"]
        __import__(modulename)
        module = sys.modules[modulename]
        #    Get the class itself
        theclass = module.__dict__[classname]
        return theclass.from_json(obj)        

    return obj

def load(path):
    with open(path, "r") as f:
        return json.load(f, object_hook=from_json)

def save(path, obj):
    with open(path, 'w') as f:
        json.dump(obj, f, default=to_json, sort_keys=True, indent=4)   