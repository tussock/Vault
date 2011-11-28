# -*- coding: utf-8 -*-
# Copyright 2010, 2011 Paul Reddy <paul@kereru.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.

import sqlite3
import sys
import os
from collections import namedtuple
from datetime import datetime
import threading


from lib import const
from lib import utils
from lib import db_sql

#    Do last!
from lib.logger import Logger
log = Logger('library')


#    Information about a version of an fs entry
#    NOTE: THIS MUST MATCH THE RETURN VALUE OF THE VIEWS BELOW
#version = namedtuple('version', 'run_id fs_id name parent_id type mod_time size version_id')
class version():
    def __init__(self, run_id, fs_id, name, parent_id, _type, mod_time, size, version_id):
        self.run_id = run_id
        self.fs_id = fs_id
        self.name = name
        self.parent_id = parent_id
        self.type = _type
        if mod_time is None:
            self.mod_time = None
        elif type(mod_time) == datetime:
            #    Make sure mod_time is a datetime object
            self.mod_time = mod_time
        else:
            self.mod_time = datetime.strptime(mod_time, const.DateTimeFormat)
            
        self.size = size
        self.version_id = version_id
    def __str__(self):
        return "Version(%s: version id %d fs_id %d parent_id %d mod_time %s run_id %d)" % \
                (self.name, self.version_id, self.fs_id, self.parent_id, str(self.mod_time), self.run_id)
#    Information about an fs entry.
#    Path is the full path. Name is just the last component
fs = namedtuple('fs', 'fs_id name parent_id')
#    Information about a run
#run = namedtuple('run', 'run_id name store type start_time hash size nfiles nfolders packages status')
class run():
    def __init__(self, run_id, name, store, _type, start_time, hash, size, nfiles, nfolders, packages, status):
        self.run_id = run_id
        self.name = name
        self.store = store
        self.type = _type

        if start_time is None:
            self.start_time = None
        elif type(start_time) == datetime:
            #    Make sure mod_time is a datetime object
            self.start_time = start_time
            self.start_time_str = datetime.strftime(self.start_time, const.DateTimeFormat)
        else:
            self.start_time = datetime.strptime(start_time, const.DateTimeFormat)
            self.start_time_str = start_time
        
        self.hash = hash
        self.size = size
        self.nfiles = nfiles
        self.nfolders = nfolders
        self.packages = packages
        self.status = status
    def __str__(self):
        return "Run(run_id %d backup %s store %s type %s start_time %s status %s hash %s)" % \
                (self.run_id, self.name, self.store, self.type, str(self.start_time), self.status, self.hash)
    
    @property
    def folder(self):
        return os.path.join(self.name, self.start_time_str + " " + self.type)
    
#    Info about a message
message = namedtuple('message', 'message_id run_id time message')
#    Info about usage
usage = namedtuple("usage", 'name size nfiles nfolders')


def db_datetime_to_datetime(db_date):
    dt = datetime.strptime(db_date, const.DateTimeFormat)
    return dt.strftime(const.ShortDateTimeFormat)


threads_db_conn = {}
threads_db_cursor = {}

class DB():
    '''
    Our interface to the DB
    
    Note that some objects are created, and then passed around between threads.
    The connection object to SQLITE cannot be passed between threads.
    
    So this DB object will keep a pool of connection objects, one per thread.
    Because all calls are transactional (i.e. a single call here, when complete
    is completely complete) that means all objects inside a thread can share
    the connection object.
    '''
    def __init__(self):
        #    Make sure the folder exists. An exception is fatal
        utils.makedirs(const.DataDir)
        #    We permit a 'selected' entry to be kept fs = current file/dir
        self.sel_fs = None
        self.sel_fs_path = None
        self.cur_run_id = None
        self.cur_store = None
        self.sel_cache = {}
        self.fs_saved_cache = []


    def check_upgrade(self):
        #    Build tables if required. Upgrade if required.
        #    Rebuilds views
        try:
            views_rebuild = False
            self.cursor.execute("select value from system where name = 'dbversion'")
            row = self.cursor.fetchone()
            if not row:
                dbversion = None
            dbversion = int(row[0])
        except Exception as e:
            dbversion = None
        log.debug("Database at version", dbversion)
        try:
            if dbversion is None:
                #    Build the tables from scratch
                log.info("Building new database")
                self.conn.executescript(db_sql.tables)
                self.conn.commit()
                dbversion = db_sql.CurrentDBVersion
                views_rebuild = True

            #    Look for upgrades
            if dbversion < db_sql.CurrentDBVersion:
                log.info("Database upgrade required")
                views_rebuild = True
            else:
                log.debug("Database upgrade not required")

            while dbversion < db_sql.CurrentDBVersion:
                if dbversion + 1 in db_sql.upgrades:
                    log.info("Upgrading the database from %d to %d" % (dbversion, dbversion + 1))
                    self.conn.executescript(db_sql.upgrades[dbversion + 1])
                    self.conn.commit()
                dbversion += 1

            #    Any database change will require the views to be rebuilt.
            if views_rebuild:
                log.debug("Rebuilding DB views")
                self.conn.executescript(db_sql.views)
                self.conn.commit()

            log.debug("Database checks complete")
        except Exception as e:
            raise Exception("Unable to update tables (%s)" % str(e))


    @property
    def cursor(self):
        #    Does the current thread already have a connection object
        thread_id = threading.current_thread().ident
        global threads_db_cursor
        if thread_id in threads_db_cursor:
            #    Reusing
            log.trace("Reusing DB cursor for thread id ", thread_id)
            _cursor = threads_db_cursor[thread_id]
        else:
            log.trace("New DB cursor thread id ", thread_id)
            _cursor = self.conn.cursor()
            threads_db_cursor[thread_id] = _cursor
        return _cursor

    @property
    def conn(self):
        #    Does the current thread already have a connection object
        thread_id = threading.current_thread().ident
        global threads_db_conn
        if thread_id in threads_db_conn:
            #    Reusing
            log.trace("Reusing DB connection for thread id ", thread_id)
            _conn = threads_db_conn[thread_id]
        else:
            log.trace("New DB connect thread id ", thread_id)
            _conn = sqlite3.connect(const.DataFile)
            threads_db_conn[thread_id] = _conn
            cur = _conn.cursor()
            cur.execute("PRAGMA journal_mode=WAL;")
            _conn.commit()
        return _conn

    def query(self, qry, args):
        self.cursor.execute(qry, args)
        return self.cursor.fetchall()

    def execute(self, qry, args):
        self.cursor.execute(qry, args)
        self.conn.commit()


    def start_run(self, name, store, type, start_time):
        log.trace("Start Run: %s" % name)
        self.cursor.execute("INSERT into runs (name, store, type, start_time, status) values (?, ?, ?, ?, ?)",
                            (name, store, type, start_time.strftime(const.DateTimeFormat), const.StatusRunning))
        self.conn.commit()
        self.cur_run_id = self.cursor.lastrowid
        self.cur_store = store
        return self.cur_run_id

    def update_run_stats(self, size, nfiles, nfolders, packages, hash):
        self.cursor.execute("update runs set size = ?, nfiles = ?, nfolders = ?, packages = ?, hash = ? where run_id = ?",
                            (size, nfiles, nfolders, packages, hash, self.cur_run_id))
        self.conn.commit()
    def update_run_status(self, status):
        self.cursor.execute("update runs set status = ? where run_id = ?", (status, self.cur_run_id))
        self.conn.commit()

    def save_message(self, message):
        '''
        Store a message against the currently active run
        @param message:
        '''
        log.trace("Logging a message: %s" % message)
        self.cursor.execute("insert into messages (run_id, message, time) values (?, ?, ?)", (self.cur_run_id, message, datetime.now().strftime(const.DateTimeFormat)))
        self.conn.commit()


    def select_path(self, path, build=True):
        '''
        Make this path the currently selected item.
        
        Path may refer to a file or folder. It is just an entry 
        in the file system.
        
        if build is True, we build the fs records in the DB as we go, if we have to.
        Otherwise, if its not there, we raise an exception
        
        Note that the first time a backup runs, it will be building all the FS entries.
        From that point on, FS entries will generally exist, and so the runs will be
        much faster.
        
        '''
        log.trace("Select Path: ", path, "build", build)
        if self.sel_fs_path == path:
            #    Its already loaded!
            pass
        elif path == "/":
            #    Quick check for root
            self.sel_fs = fs(0, "/", 0)
        elif path in self.sel_cache:
            log.debug("Cache hit!")
            (self.sel_fs, _) = self.sel_cache[path]
            #    Reset the cache entry with the new hit time.
            self.sel_cache[path] = (self.sel_fs, datetime.now())
        else:
            #    We use head recursion, so we will load parents from the cache (if possible) or the db
            parent, name = os.path.split(path)
            parent_id = self.select_path(parent, build=build)

            #    Now load this one.
            #    To speed things up - we pull down the WHOLE directory
            #    and cache it. We know we are going to need it sometime.
            try:
                self.cursor.execute("SELECT fs_id, name, parent_id FROM fs WHERE parent_id = ?",
                                (parent_id,))
                rows = self.cursor.fetchall()
                if not rows:
                    raise Exception("Missing/empty parent folder")
                #    Walk through each entry, adding it to the cache.
                dt = datetime.now()
                self.sel_fs = None
                for row in rows:
                    #    For each entry in this folder... add it into the cache.
                    fs_entry = fs(*row)
                    p = os.path.join(parent, fs_entry.name)
                    self.sel_cache[p] = (fs_entry, dt)
                    #    This is the one we were actually hunting for
                    if fs_entry.name == name:
                        self.sel_fs = fs_entry
                if not self.sel_fs:
                    raise Exception("Missing fs entry")
            except:
                if not build:
                    raise Exception("Missing path")
                #    Otherwise we build the path
                log.debug("Adding new FS entry", path)
                self.cursor.execute("INSERT INTO fs (name, parent_id) VALUES (?, ?)",
                                    (name, parent_id))
                self.conn.commit()
                fs_id = self.cursor.lastrowid
                self.sel_fs = fs(fs_id, name, parent_id)
                #    Add it to the cache
                self.sel_cache[path] = (self.sel_fs, datetime.now())

            if len(self.sel_cache) > const.FSCacheSize:
                self.trim_cache()


        self.sel_fs_path = path
        return self.sel_fs.fs_id

    def trim_cache(self):
        '''
        Trim 50% of the file system cache. 
        
        Always delete the 1/2 that is oldest.
        '''
        log.debug("Cache trim: len=", len(self.sel_cache))
        cache = [(path, item[0], item[1]) for path, item in self.sel_cache.iteritems()]
        cache.sort(key=lambda item: item[2])
        cache_len = len(cache)
        cache = cache[cache_len // 2:]
        self.sel_cache = {}
        for item in cache:
            self.sel_cache[item[0]] = (item[1], item[2])
        log.debug("final cache dict len", len(self.sel_cache))

    def get_fs(self, fs_id):
        log.trace("get_fs fs_id = ", fs_id)
        self.cursor.execute("SELECT * FROM fs where fs_id = ?", (fs_id,))
        item = self.cursor.fetchall()[0]
        #    Convert the list into a dict on the name
        return fs(*item)


    def fs_saved_old(self, path, mod_time, size, fstype='F'):
        log.trace("FS Entry Saved: ", path, mod_time, size)
        self.select_path(path)

        self.cursor.execute("INSERT INTO versions (run_id, fs_id, type, mod_time, size) VALUES (?, ?, ?, ?, ?)",
                            (self.cur_run_id, self.sel_fs.fs_id, fstype, mod_time, size))
        self.conn.commit()

    def fs_saved(self, path, mod_time, size, fstype='F'):
        log.trace("FS Entry Saved: ", path, mod_time, size)
        self.select_path(path)
        self.fs_saved_cache.append((self.cur_run_id, self.sel_fs.fs_id, fstype, mod_time, size))
        
        if len(self.fs_saved_cache) > const.FSCacheSize:
            self.fs_saved_commit()
    
    def fs_saved_commit(self):
        log.debug("fs_saved_commit saving. len=", len(self.fs_saved_cache))
        if len(self.fs_saved_cache) > 0:
            self.cursor.executemany("INSERT INTO versions (run_id, fs_id, type, mod_time, size) VALUES (?, ?, ?, ?, ?)",
                            self.fs_saved_cache)
            self.conn.commit()
            self.fs_saved_cache = []
#            size = sum([entry[4] for entry in self.fs_saved_cache])
#            #    Now also update the space used with what has just been written from the cache
#            
#            self.cursor.execute("update runs set size = size + ? where run_id = ?", (size, self.cur_run_id))
#            self.conn.commit()
            
        
    def fs_deleted(self, path):
        '''
        We use this call to record that an fs entry was deleted. We dont know
        if it was a file or folder.
        
        @param path:
        '''
        log.info("FS Entry Deleted: ", path)
        self.select_path(path)


        t = datetime.now().strftime(const.DateTimeFormat)

        self.cursor.execute("INSERT INTO versions (run_id, fs_id, type, mod_time, size) VALUES (?, ?, ?, ?, ?)",
                            (self.cur_run_id, self.sel_fs.fs_id, "X", t, 0))
        self.conn.commit()


    def list_versions_dir(self, path, build=True):
        '''
        List all versions of all files/folders in the given folder
        (path refers to a folder)
        Returns a list.
        Raises exception if the path doesn't exist
        @param path:
        '''
        self.select_path(path, build)
        return self.list_versions_dir_id(self.sel_fs.fs_id)

    def list_versions_dir_id(self, parent_id):
        log.trace("list versions dir id. id = ", parent_id)
        self.cursor.execute("SELECT * FROM all_versions " +
                            " WHERE parent_id = ? ",
                                (parent_id,))
        items = self.cursor.fetchall()
        #    Convert the list into a dict on the name
        items = list([version(*item) for item in items])
        return items


    def list_versions_file(self, path, build=True):
        '''
        List all versions of a file/folder
        Returns a list.
        
        Raises exception if the path doesn't exist
        @param path:
        '''
        self.select_path(path, build)
        return self.list_versions_file_id(self.sel_fs.fs_id)

    def list_versions_file_id(self, fs_id):
        log.trace("list versions fs id. id = ", fs_id)
        self.cursor.execute("SELECT * FROM all_versions " +
                            " WHERE fs_id = ? ",
                                (fs_id,))
        items = self.cursor.fetchall()
        #    Convert the list into a dict on the name
        items = list([version(*item) for item in items])
        return items




    def list_dir(self, path, run_id=None, build=True):
        self.select_path(path, build)
        return self.list_dir_id(self.sel_fs.fs_id, run_id)

#    def list_dir_id(self, fs_id, run_id = None):
#        #    1: Get details on the run
#        if run_id:
#            run = self.run_details(run_id)
#        else:
#            run = None
#        
#        #    2: list all versions of all files in the given folder
#        qry
    def list_dir_id(self, fs_id, run_id=None):
        '''
        Fetch the latest version for all fs entries for a given dir.
        
        Returns a DICT of the folder contents
        
        If they have versions (i.e. have been backed up) then
        the version detail for the most recent version before the
        given run.
        statuses
        Note that the latest version could be type 'X' (deleted).
        
        @param fs_id:
        @param run_id:
        '''

        qry = """
            --    Return all data for files WITH version data, where it was backed up 
            --    in or before the given run
            SELECT
                run_id,
                versions.fs_id, 
                fs.name, 
                fs.parent_id,
                type,
                mod_time,
                size,
                versions.version_id
            FROM 
                versions inner join fs using (fs_id)
                inner join (
                        --    On or before a given run, return the latest version
                        SELECT 
                            fs_id,
                            max(version_id) as version_id
                        from 
                            fs inner join versions using (fs_id)
                        WHERE
                            run_id <= ?
                            AND parent_id = ?
                        GROUP BY 
                            fs_id
            ) using (fs_id, version_id)
            
            UNION
            -- Return all fs entries in this folder that have never been backed up (no version record)
            SELECT
                NULL run_id,
                fs.fs_id, 
                fs.name,
                fs.parent_id,
                NULL type,
                NULL mod_time,
                NULL size,
                NULL version_id
            FROM 
                fs
            WHERE
                parent_id = ? AND
                fs_id not in  (select distinct fs_id from versions where versions.fs_id = fs.fs_id)

        """
        if run_id is None:
            run_id = sys.maxint
        self.cursor.execute(qry, (run_id, fs_id, fs_id))
        items = self.cursor.fetchall()
        #    Convert the list into a dict on the name
        d = dict([(item[2], version(*item)) for item in items])
        log.debug("completed list_dir_id for fsid: ", fs_id, "run_id=", run_id if run_id else "None", "results: ", d)
        return d


    def count_runs(self):
        self.cursor.execute("SELECT count(*) FROM runs")
        return self.cursor.fetchone()[0]

    def runs(self, backupname=None, start_time=None):
        '''
        Return a list of runs.
        
        If backupname is provided, this returns all runs for that backup.
        If start_time *is also* provided, then it returns only that run.
        If neither are provided, it returns all runs.
        
        @param backupname:
        @param start_time:
        '''
        #    Now load the latest versions of all files
        if backupname:
            if start_time:
                self.cursor.execute("SELECT * FROM runs where name = ? and start_time = ?", (backupname, datetime.strftime(start_time, const.DateTimeFormat)))
            else:
                self.cursor.execute("SELECT * FROM runs where name = ? order by start_time", (backupname,))
        else:
            self.cursor.execute("SELECT * FROM runs order by start_time, name")
        items = self.cursor.fetchall()
        #    Convert to a list of named tuples
        l = list([run(*item) for item in items])
        log.debug("completed runs")
        return l

    def run_details(self, run_id):
        log.trace("run_details")
        self.cursor.execute("SELECT * FROM runs where run_id = ? ", (run_id,))
        item = self.cursor.fetchone()
        if not item:
            raise Exception("Missing run (%d)" % run_id)
        
        r = run(*item)
        log.trace("done run_details")
        return r


    def run_contents(self, run_id, limit=None):
        '''
        For the current run, fetch a list of files/folders
        and details for the contents.
        
        This list could potentially be very very large. So we permit
        the creation of limits on the rows returned.
        '''
        log.trace("Run contents")
        #    Now load the latest versions of all files. 
        if limit:
            self.cursor.execute("SELECT * FROM run_versions where run_id = ? ORDER BY fs_id LIMIT ? ", (run_id, limit))
        else:
            self.cursor.execute("SELECT * FROM run_versions where run_id = ? ORDER BY fs_id", (run_id,))
        items = self.cursor.fetchall()

        #    Convert to a list of named tuples
        l = list([version(*item) for item in items])
        log.trace("Completed run contents. len=%d" % len(l))
        return l

    def run_messages(self, run_id):
        '''
        For the current run, fetch a list of messages
        raised during the run.
        '''
        log.trace("Run messages")
        #    Now load the latest versions of all files
        self.cursor.execute("SELECT * FROM messages where run_id = ? order by message_id", (run_id,))
        items = self.cursor.fetchall()

        #    Convert to a list of named tuples
        l = list([message(*item) for item in items])
        log.trace("Completed run messages. len=%d" % len(l))
        return l

    def backup_messages(self, backupname):
        '''
        For a given backup, fetch a list of messages
        raised by all runs.
        '''
        log.trace("backup messages")
        #    Now load the latest versions of all files
        self.cursor.execute("SELECT messages.* FROM messages inner join runs using  (run_id) where runs.name = ? order by message_id", (backupname,))
        items = self.cursor.fetchall()

        #    Convert to a list of named tuples
        l = list([message(*item) for item in items])
        log.trace("Completed backup messages. len=%d" % len(l))
        return l

    def messages(self):
        '''
        Fetch a list of all messages
        '''
        log.trace("messages")
        #    Now load the latest versions of all files
        self.cursor.execute("SELECT * FROM messages")
        items = self.cursor.fetchall()

        #    Convert to a list of named tuples
        l = list([message(*item) for item in items])
        log.trace("Completed messages. len=%d" % len(l))
        return l


    def run_states(self):
        '''
        Return the STATUS of the last RUN for each backup
        '''
        log.trace("Run states")
        #    Now load the latest versions of all files
        self.cursor.execute("SELECT * FROM run_states order by name")
        items = self.cursor.fetchall()

        #    Convert to a list of named tuples
        d = dict([(item[1], run(*item)) for item in items])
        log.trace("Completed run messages. len=%d" % len(d))
        return d


    def store_usages(self):
        '''
        Return the amount of space used in each store
        '''
        log.trace("Store Usages")
        #    Now load the latest versions of all files
        self.cursor.execute("SELECT * FROM store_usage order by store")
        items = self.cursor.fetchall()
        #    Convert to a list of named tuples
        d = dict([(item[0], usage(*item)) for item in items])
        log.trace("Completed store usage. len=%d" % len(d))
        return d

    def store_usage(self, store):
        #    Now load the latest versions of all files
        self.cursor.execute("SELECT * FROM store_usage where store = ?", (store,))
        items = self.cursor.fetchall()
        if len(items) == 0:
            return usage(store, 0, 0, 0)
        else:
            u = usage(*items[0])
            return u


    def store_runs(self, store):
        '''
        Return a list of runs that use this store.
        
        @param name:
        @type name:
        '''
        log.trace("Store Runs")
        self.cursor.execute("SELECT runs.* FROM runs where store = ? order by run_id", (store,))
        items = self.cursor.fetchall()

        #    Convert to a list of named tuples
        d = list([run(*item) for item in items])
        log.trace("Completed store runs. len=%d" % len(d))
        return d


    def delete_store(self, store):
        '''
        Delete a store, all runs, versions and messages related to that store
        
        @param run_id:
        @type run_id:
        '''
        self.cursor.execute("delete from messages where run_id in (select run_id from runs where store = ?)", (store,))
        self.cursor.execute("delete from versions where run_id in (select run_id from runs where store = ?)", (store,))
        self.cursor.execute("delete from runs where store = ?", (store,))
        self.conn.commit()


    def delete_run(self, run_id):
        '''
        Delete a run, and all versions stored on that run
        Also deletes messages related to that run
        
        @param run_id:
        @type run_id:
        '''
        self.cursor.execute("delete from messages where run_id = ?", (run_id,))
        self.cursor.execute("delete from versions where run_id = ?", (run_id,))
        self.cursor.execute("delete from runs where run_id = ?", (run_id,))
        self.conn.commit()

    def delete_backup(self, backupname):
        '''
        Delete a backup - which means all runs, and all versions stored on those runs
        Also deletes messages related to those runs
        
        @param run_id:
        @type run_id:
        '''
        self.cursor.execute("delete from messages where run_id in (select run_id from runs where name = ?)", (backupname,))
        self.cursor.execute("delete from versions where run_id in (select run_id from runs where name = ?)", (backupname,))
        self.conn.commit()
        self.cursor.execute("delete from runs where name = ?", (backupname,))
        self.conn.commit()

    def delete_run_versions(self, run_id):
        '''
        Delete all versions stored on a run
        This is usually done when the run fails. We delete all versions
        and remote data. But we keep the run and messages.
        
        @param run_id:
        @type run_id:
        '''
        self.cursor.execute("delete from versions where run_id = ?", (run_id,))
        self.conn.commit()

