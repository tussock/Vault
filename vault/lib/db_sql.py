# -*- coding: utf-8 -*-
# Copyright 2010, 2011 Paul Reddy <paul@kereru.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.


#####################################################################################
#
#    Current Version
#
#####################################################################################
#    Any change to the tables or views below requires an update to the
#    current DB version. If there were structural changes (such as adding
#    a column to a table), then you MUST add an upgrade[n] script, where 'n' is
#    the new version number.
CurrentDBVersion = 3

#####################################################################################
#
#    Tables
#
#####################################################################################
#    The following script will build the most recent version of the database.
#    It is only used when rebuilding from scratch (say, after a new install).
#    At all other times, we use the upgrade scripts.
tables = """

create table if not exists
    system
    (
        name TEXT PRIMARY KEY,
        value TEXT
    );
--    Current version of the database schema
insert or replace into system (name, value) values ("dbversion", "%d");

create table if not exists 
    runs 
    (
        run_id INTEGER PRIMARY KEY AUTOINCREMENT, 
        name TEXT NOT NULL,                          --    name of the backup
        store TEXT NOT NULL,                                --    name of the store where this was saved
        type TEXT NOT NULL,
        start_time TEXT NOT NULL,
        hash TEXT,
        size INTEGER DEFAULT 0 CHECK (size >= 0),              --    total bytes backed up
        nfiles INTEGER DEFAULT 0 CHECK (nfiles >= 0),            --    total files backed up. DOES NOT INCLUDE packages
        nfolders INTEGER DEFAULT 0 CHECK (nfolders >= 0),          --    total folders marked as changed 
        packages INTEGER DEFAULT 0 CHECK (packages in (0, 1)),      --    was the package list included?
        status TEXT NULL CHECK (status in ("Running", "Success", "Failed"))  --    status of the backup. One of Success, Failed, Running
    );
    
create index if not exists runs_name_idx on runs (name);

create table if not exists 
    messages 
    (
        message_id INTEGER PRIMARY KEY AUTOINCREMENT, 
        run_id INTEGER NOT NULL REFERENCES runs(run_id), 
        time text NOT NULL,
        message TEXT NOT NULL
    );
    create index if not exists messages_run_id_idx on messages (run_id);

--    This table represents entities that are found in a file system.
--    Entities can refer to files or folders, and even both (as an entity
--    can switch from a folder to file, or be removed.
--    A row here implies a name has been used at some point in a folder.
--    It may or may not be used now. It may switch types. 
--    Optimisation: added path to speed finding paths.
create table if not exists
    fs
    (
        fs_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        parent_id INTEGER NOT NULL REFERENCES fs (fs_id)
    );
create index if not exists fs_name_idx on fs (name);
create index if not exists fs_parent_id_idx on fs (parent_id, fs_id);


--    Make sure the special entry - ROOT - exists.
insert or ignore into fs (fs_id, name, parent_id) values (0, "/", 0);

--    Versions table. There is one entry for each file/folder saved during
--    a backup run.
--    Type has the following values:
--        "D": this was a directory entry. size will always be 0
--        "F": this was a file entry. 
--        "X": this is a delete (i.e. the file was removed. This means
--                the file was backed up during a previous run
--                but now does not exist).
--    Note that fs entries can change type (file->folder->file). So the
--    type is fixed only at a point in time (a version).

create table if not exists 
    versions 
    (
        version_id INTEGER PRIMARY KEY AUTOINCREMENT, 
        run_id INTEGER NOT NULL REFERENCES runs(run_id),
        fs_id INTEGER NOT NULL REFERENCES files(file_id),
        type TEXT NOT NULL CHECK (type in ('F', 'D', 'X')), 
        --    NOTE: bug in sqlite. Inclusion in LEFT OUTER join
        --    seems broken unless these default to a NON NULL.
        mod_time TEXT DEFAULT "", 
        size INTEGER DEFAULT 0
    );
create index if not exists versions_run_id_idx on versions (run_id, fs_id);
create index if not exists versions_fs_id_idx on versions (fs_id, version_id);


""" % CurrentDBVersion

#####################################################################################
#
#    Upgrade Scripts
#
#####################################################################################

#    upgrade[n] will upgrade the database from n-1 to n.
#    So to upgrade from version a to version b, we run the scripts:
#        upgrades[a+1]
#        upgrades[a+2]
#        ...
#        upgrades[b]
upgrades = {}

upgrades[2] = """
update system set value = 2 where name = 'dbversion';
"""
#    The view are a simple script to build all views. It is run
#    anytime the database is upgraded (after the last upgrade completes)
views = """
    
--    Return all versions for all files.
--    select * from all_versions where fs_id = ?
drop view if exists all_versions;
CREATE VIEW all_versions as
SELECT 
    run_id,
    fs_id, 
    name, 
    parent_id,
    type, 
    mod_time, 
    size,
    version_id 
FROM 
    fs LEFT OUTER JOIN versions USING (fs_id)
ORDER BY
    versions.version_id;
    
DROP VIEW IF EXISTS run_versions;
CREATE VIEW run_versions AS
select 
    runs.run_id,
    fs.fs_id fs_id,
    fs.name,
    parent_id,
    versions.type,
    mod_time,
    versions.size,
    version_id
FROM
    versions inner join runs using (run_id)
    inner join fs using (fs_id);

DROP VIEW IF EXISTS run_states;
CREATE VIEW run_states AS
SELECT 
    * 
FROM 
    runs 
GROUP BY 
    name 
HAVING 
    run_id = max(run_id);
    
DROP VIEW IF EXISTS store_usage;
CREATE VIEW store_usage AS
SELECT
    store,
    sum(size) as total_size,
    sum(nfiles) as total_files,
    sum(nfolders) as total_folders
FROM 
    runs
GROUP BY 
    store;
    
DROP VIEW IF EXISTS backup_size;
CREATE VIEW backup_size AS
SELECT
    name,
    sum(size)
FROM 
    runs
GROUP BY 
    name;
    
DROP VIEW IF EXISTS running_backup_sizes;
CREATE VIEW running_backup_sizes AS
SELECT 
    runs.store as store, 
    sum(versions.size) as total_size
FROM 
    versions INNER JOIN runs USING (run_id) 
WHERE 
    runs.status = 'Running'
GROUP BY 
    runs.store;


    
"""
