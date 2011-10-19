# -*- coding: utf-8 -*-
# Copyright 2010, 2011 Paul Reddy <paul@kereru.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.

'''
Save an object to XML.
Used to save settings.

All class objects and builtin types are saved.

When handed a class, the class is streamed out to the given file.

Note that on loading, __init__ is *not* called. A blank class is created,
all attributes are loaded in to it, then its class is reassigned.
This is all you need for simple classes that hold data.

HOWEVER there are several systems which support creating an object properly
if required. These are defined below.

Systems for loading a class:
a) By default, attributes starting with "_" are deemed temporary and not loaded
b) Use a "_persistence" list of names. Only these will be loaded. Remember
to increase "_persistence" in your subclasses
c) If your class has a "post_load" function defined, then that will be called
after loading.
d) If your class has a "copy" classmethod, then that will be called to
copy the loaded object. The copy classmethod should call the __init__ as
required, then fix up the class internals. Postload may then be called.

 
'''
from __future__ import with_statement, print_function
import xml.etree.ElementTree as et
import sys

class UnknownClassException(Exception):
    pass

class BlankClass(object):
    pass


class XMLSettings:
    def __init__(self, filename="settings.xml"):
        self.filename = filename


    def save(self, obj):
        tree = et.Element("__toplevel__")
        self.output(obj, "root", tree)
        et.ElementTree(tree[0]).write(self.filename)

    def outputsimple(self, obj, name, parent):
        node = et.SubElement(parent, name, {"type": obj.__class__.__name__})
        node.text = str(obj)

    def outputnone(self, name, parent):
        dummy = et.SubElement(parent, name, {"type": "none"})

    def outputdict(self, obj, name, parent):
        node = et.SubElement(parent, name, {"type": obj.__class__.__name__})
        for (key, value) in obj.iteritems():
            item = et.SubElement(node, "item")
            self.output(key, "key", item)
            self.output(value, "value", item)

    def outputlist(self, obj, name, parent):
        node = et.SubElement(parent, name, {"type": obj.__class__.__name__})
        for value in obj:
            self.output(value, "attr", node)

    def outputcomplex(self, obj, name, parent):
        node = et.SubElement(parent, name, {"type": obj.__class__.__name__})
        self.output(obj.real, "real", node)
        self.output(obj.imag, "imag", node)

    def output(self, obj, name, parent):
        if name[0] == "_":
            return
        #    Check for builtin types
        if obj.__class__ in (int, str, bool, float, long, unicode):
            self.outputsimple(obj, name, parent)
        elif obj.__class__ == dict:
            self.outputdict(obj, name, parent)
        elif obj.__class__ in (list, tuple):
            self.outputlist(obj, name, parent)
        elif obj.__class__ == complex:
            self.outputcomplex(obj, name, parent)
        elif obj.__class__ == type(None):
            self.outputnone(name, parent)
        else:
            #    Its a class object. 
            node = et.SubElement(parent, name,
                                {"type": obj.__class__.__name__,
                                 "module": obj.__class__.__module__})
            if hasattr(obj, "_persistent"):
                #    Only output persistent fields
                for nm in obj._persistent:
                    value = obj.__dict__[nm]
                    self.output(value, nm, node)
                #    Must save the persistent node itself
                self.output(obj._persistent, "_persistent", node)
            else:
                #    Output all fields
                for nm in obj.__dict__:
                    if nm[0] == "_":
                        continue
                    value = obj.__dict__[nm]
                    self.output(value, nm, node)

    def load(self, defaults=None):
        tree = et.parse(self.filename)
        root = tree.getroot()
        ret = self.loadobject(root, defaults)
        return ret

    def loadobject(self, node, defaults=None):
#        global classes                
#        Only necessary if we assign
        #    If its a builtin, we just return that.
        _type = node.get("type")
        name = node.tag
        value = node.text
        if _type == "int":
            ret = int(value)
        elif _type == "str" or _type == "unicode":
            if node.text == None:
                ret = ""
            else:
                ret = node.text
        elif _type == "bool":
            ret = node.text.lower() == "true"
        elif _type == "float":
            ret = float(node.text)
        elif _type == "long":
            ret = long(node.text)
        elif _type == "none":
            ret = None
        elif _type == "complex":
            real = self.loadobject(node.find("real"))
            imag = self.loadobject(node.find("imag"))
            ret = complex(real, imag)
        elif _type == "list":
            ret = []
            for child in node:
                ret.append(self.loadobject(child))
        elif _type == "tuple":
            l = []
            for child in node:
                l.append(self.loadobject(child))
            ret = tuple(l)
        elif _type == "dict":
            ret = {}
            for child in node:
                key = self.loadobject(child.find("key"))
                value = self.loadobject(child.find("value"))
                ret[key] = value
        else:
            #    Its some type of class.

            #    Get the reference to the class
            modulename = "unknown"
            try:
                #    1a: Get the class's module and import it
                modulename = node.get("module")
                __import__(modulename)
                module = sys.modules[modulename]
                #    1b: Get the class itself
                theclass = module.__dict__[_type]
            except:
                #    If we can't find the module or class
                raise UnknownClassException("Can't find " + _type + " in module " + modulename)

            #    2: Create a blank class
#            if defaults:
#                ret = defaults
#            else:
            ret = theclass()

            #    3: Load in all data
            for child in node:
                name = child.tag
                value = self.loadobject(child)
                ret.__dict__[name] = value

            #    4: Set the correct class
            #if not defaults:
            #    ret.__class__ = theclass

            #    5: If we have a copy constructor available - use it to properly configure the object
            if hasattr(ret, "copy"):
                ret = ret.copy()
            #    6: If the class has a post-load function, call it.
            if hasattr(ret, "post_load"):
                ret.post_load()

        return ret



