# Copyright 2010, 2011 Paul Reddy <paul@kereru.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.

'''
Created on Nov 9, 2010

@author: paul
'''

from threading import Thread
import hashlib
import os


from lib import const

#    Do this last!
from lib.logger import Logger
log = Logger("io")

class StreamBase():
    def __init__(self, folder, basename):
        self.folder = folder
        self.basename = basename
    
    def get_path(self, chunk_number):
        folderno = chunk_number // const.ChunksPerFolder
        fileno = chunk_number % const.ChunksPerFolder     
        fname = os.path.join(self.folder, "data", "%05d" % folderno, self.basename+"%03d" % fileno)
        return fname
        
class StreamOut(Thread, StreamBase):
    def __init__(self, stream, store, folder, basename="data"):
        '''
        Stream data t a store.
        The datastream will be split into chunks for reliable
        transmission.
        At the end, the stream will not be closed (unless there was an error)
        
        @param store: the store object to be used
        @param folder: The folder where these files will be stored
        @param basename: The root name of the file. It will have a 
                number added to it
                    
        @param stream: the input stream. It will be read until EOF.
        '''
        Thread.__init__(self, name="StreamOut")
        StreamBase.__init__(self, folder, basename)
        log.info("Building Streamer object")
        self.stream = stream
        self.store = store

        log.debug("Streamer construction complete")
        #    If we get an error during execution, it will be stored here.
        self.error = None
        
        self.total_bytes = 0
        self.hashobj = hashlib.sha256()

    def run(self):
        try:
            self.store.connect()
            chunk_bytes = 0
            chunk_number = 0
            fd = self.store.open(self.get_path(chunk_number), "wq")
            
            self.store.check_space(self.total_bytes)
            
            try:
                while True:
                    buffer = self.stream.read(const.BufferSize)
                    self.hashobj.update(buffer)
                    if len(buffer) == 0:
                        break
                    if chunk_bytes + len(buffer) > const.ChunkSize:
                        #    Write what we can
                        to_write = const.ChunkSize - chunk_bytes
                        fd.write(buffer[0:to_write])
                        fd.close()
                        #    Create new chunk
                        chunk_number += 1
                        fd = self.store.open(self.get_path(chunk_number), "wq")
                        #    Write the rest
                        fd.write(buffer[to_write:])
                        chunk_bytes = len(buffer) - to_write
                        
                        #    With each new chunk - we re-check the space avail
                        self.store.check_space(self.total_bytes)
                    else:
                        fd.write(buffer)
                        chunk_bytes += len(buffer)
                    self.total_bytes += len(buffer)
                #    At the end we give a final space check
                self.store.check_space(self.total_bytes)
                return
            finally:
                fd.close()
                self.store.disconnect()
        except Exception as e:
            #    Any problems are returned to the main thread via an error object.
            self.error = e
            log.error("Got error in streamer run:", str(e))
            #    If something went wrong, we try to close the pipe to ensure
            #    the callers know about it. Make sure this can't fail.
            try:
                self.stream.crash()
            except:
                pass
            log.debug("Streamer terminating")
            
    def get_hash(self):
        return (self.total_bytes, self.hashobj.hexdigest())

class StreamIn(Thread, StreamBase):
    def __init__(self, stream, store, folder, basename="data"):
        '''
        Streaming data from a distant location (the store)
        This class will close the stream when the remote location is fully 
        streamed.
        '''
        Thread.__init__(self, name="StreamIn")
        StreamBase.__init__(self, folder, basename)
        log.info("Building Streamer object")
        self.stream = stream
        self.store = store

        log.debug("Streamer construction complete")
        #    If we get an error during execution, it will be stored here.
        self.error = None
        self.total_bytes = 0
        self.hashobj = hashlib.sha256()


    def run(self):
        chunk_bytes = 0
        chunk_number = 0
        
        try:
            self.store.connect()
            try:
                fd = self.store.open(self.get_path(chunk_number), "r")
                #    There was no data
            except:
                return (None, None)
            
            while True:
                buffer = fd.read(const.BufferSize)
                if len(buffer) > 0:
                    self.stream.write(buffer)
                    #    Update counters
                    self.hashobj.update(buffer)
                    chunk_bytes += len(buffer)
#                    total_bytes += 0    #    Just a marker. Total bytes adjusted below
                else:
                    #    move to the next split
                    fd.close()
                    chunk_number += 1
                    chunk_bytes = 0
                    try:
                        log.debug("Opening chunk", chunk_number, self.get_path(chunk_number))
                        fd = self.store.open(self.get_path(chunk_number), "r")
                    except:
                        #    We have run out of splits
                        break
                self.total_bytes += len(buffer)
            self.stream.close()
        except Exception as e:
            #    Any problems are returned to the main thread via an error object.
            self.error = e
            log.debug("Got error in streamer run:", str(e))
            #    If something went wrong, we try to close the pipe to ensure
            #    the callers know about it. Make sure this can't fail.
            log.error("Closing the stream")
            try:
                self.stream.crash()
            except:
                pass
        finally:
            self.store.disconnect()
            
    def get_hash(self):
        return (self.total_bytes, self.hashobj.hexdigest())