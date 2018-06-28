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

    def __init__(self, dbfilename):
        self.basepath = dbfilename
        os.makedirs(dbfilename, exist_ok=True)

    def get(self, key1):
        std, aux = self.__key_to_path(key1)
        if os.path.isfile(std):
            with open(std, "rb") as f:
                return f.read()
        else:
            if os.path.isfile(aux):
                with open(aux) as f:
                    return f.read()
        return None

    def put(self, key1, val1):
        std, aux = self.__key_to_path(key1)
        aux = aux  # Make eclipse happy.
        os.makedirs(os.path.dirname(std), exist_ok=True)
        with open(std, "wb") as f:
            f.write(val1)

    def check(self, key1):
        std, aux = self.__key_to_path(key1)
        return os.path.isfile(std) or os.path.isfile(aux)

    def delete(self, key1):
        std, aux = self.__key_to_path(key1)
        if os.path.isfile(std):
            os.remove(std)
        if os.path.isfile(aux):
            os.remove(aux)

    def mark_start(self):
        src = self.__typ_to_path(DataStore_Tree.__std)
        des = self.__typ_to_path(DataStore_Tree.__aux)
        shutil.rmtree(des, ignore_errors=True)
        os.rename(src, des)

    def mark_mark(self, key1):
        des, src = self.__key_to_path(key1)
        dir_des = os.path.dirname(des)
        os.makedirs(dir_des)
        os.rename(src, des)

    def mark_cancel(self):
        #TODO
        None

    def mark_delete(self):
        src = self.__typ_to_path(DataStore_Tree.__aux)
        shutil.rmtree(src, ignore_errors=True)

    def __typ_to_path(self, typ):
        path = os.path.join(self.basepath, str(typ))
        return path

    def __key_to_path(self, key1):
        name = ''.join(map(lambda x: '%.2x' % x, key1))
        name = os.path.join(name[0:2], name[2:4], name[4:6], name)
        std = os.path.join(self.__typ_to_path(DataStore_Tree.__std), name)
        aux = os.path.join(self.__typ_to_path(DataStore_Tree.__aux), name)
        return (std, aux)

if __name__ == "__main__":
    import hash_sha1
    Hash_f = hash_sha1.Hash_SHA1

    ds = DataStore_Tree("/tmp/ds")
    h = Hash_f()
    h.update(b"abcdefghi")
    key1 = h.digest()
    val1 = "How now brown cow?"
    ds.delete(key1)

    print(ds.check(key1))
    assert(not ds.check(key1))

    print(ds.get(key1))
    assert(ds.get(key1) is None)

    ds.put(key1, val1)
    print(ds.check(key1))
    assert(ds.check(key1))

    print(ds.get(key1))
    assert(ds.get(key1) == val1)

    h = Hash_f()
    h.update(b"0123456789")
    key2 = h.digest()
    val2 = "Now is the time"
    ds.delete(key2)
    ds.put(key2, val2)
    print(ds.check(key2))
    assert(ds.check(key2))

    print(ds.get(key2))
    assert(ds.get(key2) == val2)

    ds.mark_start()
    assert(ds.check(key1))
    assert(ds.check(key2))
    ds.mark_mark(key2)
    assert(ds.check(key1))
    assert(ds.check(key2))
    ds.mark_delete()
    assert(not ds.check(key1))
    assert(    ds.check(key2))
    assert(ds.get(key2) == val2)

