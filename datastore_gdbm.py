#!/usr/bin/env python3

from datastore_base import DataStore

import dbm.gnu as dbm


class DataStore_Gdbm(DataStore):
    """
    Use a GDBM database to store objects.
    """

    def __init__(self, dbfilename):
        self.basepath = dbfilename
        self.db       = dbm.open(dbfilename, "cuf")

    def get(self, key1):
        return self.db.get(key1, None)

    def put(self, key1, val1):
        self.db[key1] = val1

    def check(self, key1):
        return key1 in self.db

    def delete(self, key1):
        try:
            del self.db[key1]
        except:
            pass

    def mark_start(self):
        #TODO
        pass

    def mark_mark(self, key1):
        #TODO
        pass

    def mark_cancel(self):
        #TODO
        None

    def mark_delete(self):
        #TODO
        pass

if __name__ == "__main__":
    import hash_sha1
    Hash_f = hash_sha1.Hash_SHA1

    ds = DataStore_Gdbm("/tmp/ds")
    h = Hash_f()
    h.update(b"abcdefghi")
    key1 = h.digest()
    val1 = b"How now brown cow?"
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
    val2 = b"Now is the time"
    ds.delete(key2)
    ds.put(key2, val2)
    print(ds.check(key2))
    assert(ds.check(key2))

    print(ds.get(key2))
    assert(ds.get(key2) == val2)

#     ds.mark_start()
#     assert(ds.check(key1))
#     assert(ds.check(key2))
#     ds.mark_mark(key2)
#     assert(ds.check(key1))
#     assert(ds.check(key2))
#     ds.mark_delete()
#     assert(not ds.check(key1))
#     assert(    ds.check(key2))
#     assert(ds.get(key2) == val2)
