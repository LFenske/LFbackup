#!/usr/bin/env python3

from datameta_base import DataMeta_Base

import sqlite3
import pickle
import os
import stat
import time


class DataMeta_Sqlite(DataMeta_Base):

    def __init__(self, dbname):
        self.basepath = dbname
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
                PRIMARY KEY (parent_ino, parent_dev, filename))""")
        self.conn.commit()

    def put(self, filename, is_dir, stats, depth, hsh):
        curs = self.conn.cursor()
        try:
            now = time.time()
            current = self.get(filename)
            current = current[1]  # don't need to know is_dir
            # Assume len current > 0.
            if (
                    current[0][0] == stats and
                    current[0][1] == depth and
                    current[0][2] == hsh):
                current[0][4] = now
            else:
                current.insert(0, [stats, depth, hsh, now, now])
            curs.execute(
                "UPDATE stats SET pickle = ? WHERE filename = ?",
                (pickle.dumps(current), filename))
        except:
            current = [[stats, depth, hsh, now, now]]
            curs.execute(
                "INSERT INTO stats("
                "filename,"
                "ino,"
                "dev,"
                "parent_ino,"
                "parent_dev,"
                "pickle"
                ") VALUES (?,?,?,?,?,?)",
                (
                    filename,
                    stats.st_ino,
                    stats.st_dev,
                    0,
                    0,
                    pickle.dumps(current)
                )
            )
        self.conn.commit()

    def get(self, filename):
        curs = self.conn.cursor()
        curs.execute(
            "SELECT pickle FROM stats WHERE filename IS ?",
            (filename,))
        d = curs.fetchone()
        current = pickle.loads(d[0])
        is_dir  = stat.S_ISDIR(current[0][0].st_mode)
        return (is_dir, current)

if __name__ == "__main__":
    dm = DataMeta_Sqlite("/tmp/test.db")
    fn = "datastore_tree.py"
    stats = os.lstat(fn)
    dm.put(fn, False, stats, 42, "xyzzy")

    current = dm.get(fn)
    #(is_dir, stats, depth, hsh) = dm.get(fn)
    print(current[0], current[1:])

    fn = os.getcwd()
    stats = os.lstat(fn)
    dm.put(fn[1:], True , stats, 43, "plugh")

    current = dm.get(fn[1:])
    #(is_dir, stats, depth, hsh) = dm.get(fn[1:])
    print(current[0], current[1:])
