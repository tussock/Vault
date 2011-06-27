'''
Created on May 26, 2011

@author: paul
'''

import time

class Timer():
    def __init__(self, tag="Time:"):
        self.tag = tag
        
    def __enter__(self): 
        self.start = time.time()
    def __exit__(self, *args): 
        elapsed = time.time() - self.start
        print("%s: %.02fs" % (self.tag, elapsed))