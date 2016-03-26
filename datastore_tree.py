#!/usr/bin/env python3

from datastore_base import DataStore

import os
import shutil

class DataStore_Tree(DataStore):
    """
    Use a tree in the file system to store objects.
    """
    
    __std = 0
    __aux = 1
    
    def __init__(self, basepath):
        self.basepath = basepath
        os.makedirs(basepath, exist_ok=True)

    def get(self, key):
        path = self.__key_to_path(key, DataStore_Tree.__std)
        if os.path.isfile(path):
            with open(path) as f:
                return f.read()
        else:
            path = self.__key_to_path(key, DataStore_Tree.__aux)
            if os.path.isfile(path):
                with open(path) as f:
                    return f.read()
        return None
    
    def put(self, key, val):
        path = self.__key_to_path(key, DataStore_Tree.__std)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(val)
    
    def check(self, key):
        path = self.__key_to_path(key, DataStore_Tree.__std)
        return os.path.isfile(path)
    
    def delete(self, key):
        path = self.__key_to_path(key, DataStore_Tree.__std)
        if os.path.isfile(path):
            os.remove(path)
    
    def mark_start(self):
        src = self.__typ_to_path(DataStore_Tree.__std)
        des = self.__typ_to_path(DataStore_Tree.__aux)
        shutil.rmtree(des)
        os.rename(src, des)
    
    def mark_mark(self, key):
        path_src = self.__key_to_path(key, DataStore_Tree.__aux)
        path_des = self.__key_to_path(key, DataStore_Tree.__std)
        dir_des = os.path.dirname(path_des)
        os.makedirs(dir_des)
        os.rename(path_src, path_des)
    
    def mark_cancel(self):
        None
    
    def mark_delete(self):
        src = self.__typ_to_path(DataStore_Tree.__aux)
        shutil.rmtree(src)
        
    def __typ_to_path(self, typ):
        path = os.path.join(self.basepath, str(typ))
        return path
    
    def __key_to_path(self, key, typ):
        name = ''.join(map(lambda x: '%.2x' % x, key))
        path = os.path.join(self.__typ_to_path(typ), name[0:2], name[2:4], name[4:6], name)
        return path

if __name__ == "__main__":
    ds = DataStore_Tree("/tmp/ds")
    key = b"abcdefghi"
    val = "How now brown cow?"
    ds.delete(key)
    print(ds.check(key))
    assert(not ds.check(key))
    print(ds.get(key))
    assert(ds.get(key) is None)
    ds.put(key, val)
    print(ds.check(key))
    assert(ds.check(key))
    print(ds.get(key))
    assert(ds.get(key) == val)
