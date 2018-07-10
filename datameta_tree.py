#!/usr/bin/env python3

from datameta_base import DataMeta_Base

import os.path
import pickle


class DataMeta_Tree(DataMeta_Base):

    filepath = "file"
    dirpath  = "dir"
    dirsuff  = ".d"
    dirinfo  = "info"

    def __init__(self, dbfilename):
        self.basepath = dbfilename

    def put(self, filename, is_dir, stats, depth, hsh):
        (fdir, fpath, ddir, dpath) = self.__paths(filename)
        if is_dir:
            (dire, path) = (ddir, dpath)
            os.makedirs(fpath, exist_ok=True)
        else:
            (dire, path) = (fdir, fpath)
        os.makedirs(dire, exist_ok=True)
        with open(path, "wb") as f:
            pickle.dump((stats, depth, hsh), f)

    def get(self, filename):
        (fdir, fpath, ddir, dpath) = self.__paths(filename)
        fdir = fdir  # Get rid of warning.
        ddir = ddir  # Get rid of warning.
        if   os.path.exists(dpath):
            path = dpath
            is_dir = True
        elif os.path.exists(fpath):
            path = fpath
            is_dir = False
        else:
            return None
        print("path =", path)
        with open(path, "rb") as f:
            current = pickle.load(f)
        return (is_dir, current)

    def __paths(self, filename):
        fdir  = os.path.join(self.basepath, self.filepath)
        fpath = os.path.join(fdir, filename)
        ddir  = os.path.join(self.basepath, self.dirpath, filename+self.dirsuff)
        dpath = os.path.join(ddir, self.dirinfo)
        return (fdir, fpath, ddir, dpath)

if __name__ == "__main__":
    dm = DataMeta_Tree("/tmp/testtree")
    fn = "database_tree.py"
    stats = os.lstat(fn)
    dm.put(fn, False, stats, 42, "xyzzy")

    (is_dir, stats, depth, hsh) = dm.get(fn)
    print(is_dir, stats, depth, hsh)

    fn = os.getcwd()
    stats = os.lstat(fn)
    dm.put(fn[1:], True , stats, 43, "plugh")

    (is_dir, stats, depth, hsh) = dm.get(fn[1:])
    print(is_dir, stats, depth, hsh)
