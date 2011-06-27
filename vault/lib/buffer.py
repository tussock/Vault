# -*- coding: utf-8 -*-
'''
Created on May 4, 2011

@author: paul
'''
import threading
import time

BufferSize = 102400
DefaultName = "__buffer__"

#    Do this last!
from lib.logger import Logger
log = Logger("library")


class Buffer(object):
    '''
    A buffer class accepts data via write, stores it efficiently
    in an internal buffer, then permits it to be read.
    
    If it is not closed, then readers will block if there is no data.
    If the buffer gets to big, then writers will block until the data
    is read.
    
    This is threadsafe, meaning that readers and writers can be in 
    different threads.
    
    '''
    def __init__(self, name=DefaultName, high_water=BufferSize*2):
        self.name = name
        self.high_water = high_water
        self.buffer = []
        self.length = 0
        self.closed = False
        self.lock = threading.Lock()
        self.read_bytes = 0
        self.write_bytes = 0
    
    def close(self):
        log.debug("BUFFER closed")
        self.closed = True
        
    
    def crash(self):
        '''
        Like close, but doesn't attempt any cleanup. Bypasses
        childrens attempt to write the last data.
        '''
        log.debug("BUFFER crashed")
        self.closed = True
        
    def write(self, data):
        if len(data) == 0:
            return
        if self.closed:
            raise Exception("Writing %d bytes to a closed buffer" % len(data))

        #    Check if we are too big
        while self.length > self.high_water and not self.closed:
            time.sleep(0.1)
            
        #    Buffer must have closed while we were waiting.
        #    This will usually be an error downstream
        if self.closed:
            raise Exception("Writing %d bytes to a closed buffer" % len(data))
        
            
        self.lock.acquire()
        try:
            self.buffer.append(data)
            self.length += len(data)
            self.write_bytes += len(data)
        finally:
            self.lock.release()
        log.debug("BUFFER wrote %d bytes" % len(data))
        
    def read(self, maxlen=0):
        '''
        Read will return data from the buffer.
        
        If maxlen == 0, then it will return all data it has. There may be more
        data to come. THIS IS DIFFERENT TO THE STANDARD READ which will return
        all data, blocking until it has everything.
        
        @param maxlen:
        '''
        log.trace("Buffer.read: maxlen=%d" % (maxlen))
        #    Wait for data or closure
        while self.length == 0 and not self.closed:
            time.sleep(0.1)
        
        #    No data, but closed...
        if self.length == 0 and self.closed:
            log.debug("BUFFER read closed and no data")
            return ""
        
        self.lock.acquire()
        try:
            ret = "".join(self.buffer)
            self.buffer = []
            self.length = 0
            if maxlen > 0:
                #    Put back the data that is not wanted
                if maxlen < len(ret):
                    self.buffer.append(ret[maxlen:])
                    self.length = len(self.buffer[0])
                    ret = ret[:maxlen]
                
            self.read_bytes += len(ret)
            log.debug("BUFFER read %d bytes" % len(ret))
            return ret
        finally:
            self.lock.release()
            
    def seek(self, offset, whence=0):
        pass
        
    def tell(self):
        log.debug("BUFFER tell returning 1024")
        return 10