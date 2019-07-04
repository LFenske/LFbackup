#!/usr/bin/env python3

from datastore_base import DataStore

import dbm.gnu as dbm
import pathlib
import os


class DataStore_Gdbm(DataStore):
    """
    Use a GDBM database to store objects.
    """

    rebalance = False
    max_db_size = 1500*1000*1000*1000

    def __init__(self, dbname, hashfact):
        super().__init__()
        self.basepath = dbname  # directory
        self.hashfact = hashfact  # hash factory

        # Ensure path exists.
        path = pathlib.Path(self.basepath)
        try:
            path.mkdir(parents=True)  # exist_ok=True is only for Python 3.5+
        except FileExistsError:
            pass

        # Are there any databases yet?  If not, create one.
        if len(list(path.iterdir())) == 0:
            e = self._create_db(0, hashfact.min(), hashfact.max())
            e["db"].close()  # will reopen later

        # Open all databases in order starting from the highest level.
        self.dbs = []
        for d in sorted(path.iterdir(), reverse=True):
            print(d)
            db = dbm.open(str(d), "cuf")
            e = {}
            e["db"      ] = db
            e["filename"] = db["filename"]
            e["level"   ] = db["level"   ]
            e["minhash" ] = db["minhash" ]
            e["maxhash" ] = db["maxhash" ]
            self.dbs.append(e)

    def _create_db(self, level, minhash, maxhash):
        #print("create_db: level =", level, "minhash =", minhash, " maxhash =", maxhash)
        level = str(level)
        filename = self.basepath + "/" + level + "-" + self.hashfact.hexify(minhash)[0:4] + "-" + self.hashfact.hexify(maxhash)[0:4]
        print("filename =", filename)
        e = {}
        db = dbm.open(filename, "cuf")
        db["filename"] = filename
        db["level"   ] = level
        db["minhash" ] = minhash
        db["maxhash" ] = maxhash
        e["db"      ] = db
        e["filename"] = db["filename"]
        e["level"   ] = db["level"   ]
        e["minhash" ] = db["minhash" ]
        e["maxhash" ] = db["maxhash" ]
        return e

    def get(self, key1):
        first = True
        for e in self.dbs:
            # Assuming the min/max comparison is much cheaper than testing for inclusion.
            if e["minhash"] <= key1 <= e["maxhash"]:
                if key1 in e["db"]:
                    retval = e["db"][key1]
                    if self.rebalance and not first:
                        # Delete this one and insert into first one.
                        self.put(key1, retval)
                        del e["db"][key1]
                    return retval
                first = False
        return None

    def put(self, key1, val1):
        for e in self.dbs:
            #print("min:", e["minhash"], " max:", e["maxhash"])
            if e["minhash"] <= key1 <= e["maxhash"]:
                if os.stat(e["filename"]).st_size + len(val1) > self.max_db_size:
                    # This db has gotten too big: split it.
                    # Find average of minhash and maxhash as split point.
                    splitpoint = self.hashfact.split_range(e["minhash"], e["maxhash"])
                    #print("splitpoint =", splitpoint)
                    # Create db from minhash-avg and from avg-maxhash, increasing level.
                    self.dbs.insert(0, self._create_db(int(e["level"])+1, e["minhash"], splitpoint))
                    self.dbs.insert(0, self._create_db(int(e["level"])+1, splitpoint, e["maxhash"]))
                    # Call put to insert into new db.
                    self.put(key1, val1)
                    return
                e["db"][key1] = val1
                return
        raise Exception("Can't find a db for put, key =", key1)

    def check(self, key1):
        for e in self.dbs:
            if e["minhash"] <= key1 <= e["maxhash"]:
                if key1 in e["db"]:
                    return True
        else:
            return False

    def delete(self, key1):
        for e in self.dbs:
            if e["minhash"] <= key1 <= e["maxhash"]:
                if key1 in e["db"]:
                    del e["db"][key1]

    def mark_start(self):
        # TODO
        pass

    def mark_mark(self, key1):
        # TODO
        pass

    def mark_cancel(self):
        # TODO
        None

    def mark_delete(self):
        # TODO
        pass


if __name__ == "__main__":
    import hash_sha1
    Hash_f = hash_sha1.Hash_SHA1

    ds = DataStore_Gdbm("/tmp/ds", Hash_f)
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
