#!/usr/bin/env python3

from datameta_base import DataMeta_Base

import sqlite3
import pickle
import os
import stat

class DataMeta_Sqlite(DataMeta_Base):

    def __init__(self, basepath):
        self.basepath = basepath
        self.conn = sqlite3.connect(self.basepath)
        curs = self.conn.cursor()
        curs.execute("""
            CREATE TABLE IF NOT EXISTS stats (
                filename   text,
                ino        integer,
                dev        integer,
                parent_ino integer,
                parent_dev integer,
                pickle     blob,
                PRIMARY KEY (ino, dev))""")
        self.conn.commit()

    def put(self, filename, is_dir, stats, depth, hsh):
        curs = self.conn.cursor()
        curs.execute("INSERT INTO stats(filename, ino, dev, pickle) VALUES (?,?,?,?)",
                     (filename, stats.st_ino, stats.st_dev, pickle.dumps((stats, depth, hsh))))
        self.conn.commit()

    def get(self, filename):
        curs = self.conn.cursor()
        curs.execute("SELECT pickle FROM stats WHERE filename IS ?", (filename,))
        d = curs.fetchone()
        (stats, depth, hsh) = pickle.loads(d[0])
        is_dir = stat.S_ISDIR(stats.st_mode)
        return (is_dir, stats, depth, hsh)

if __name__ == "__main__":
    dm = DataMeta_Sqlite("/tmp/test.db")
    fn = "datastore_tree.py"
    stats = os.lstat(fn)
    dm.put(fn, False, stats, 42, "xyzzy")

    (is_dir, stats, depth, hsh) = dm.get(fn)
    print(is_dir, stats, depth, hsh)

    fn = os.getcwd()
    stats = os.lstat(fn)
    dm.put(fn[1:], True , stats, 43, "plugh")

    (is_dir, stats, depth, hsh) = dm.get(fn[1:])
    print(is_dir, stats, depth, hsh)

