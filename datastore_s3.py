#!/usr/bin/env python3

from datastore_base import DataStore

import boto3
import botocore


class DataStore_S3(DataStore):
    """
    Use an S3 to store objects.
    """

    def _mapkey(self, key):
        return self.keyprefix + self.hashfact.hexify(key)

    def __init__(self, keyprefix, hashfact):
        self.keyprefix = keyprefix
        self.hashfact  = hashfact
#        self.s3 = boto3.resource("s3")
        self.s3 = boto3.resource(
            "s3",
            endpoint_url="http://localhost:9000",
            aws_access_key_id=    "minioadmin",
            aws_secret_access_key="minioadmin",
        )
        self.bucket = "lfbackup-store"

    def get(self, key1):
        key = self._mapkey(key1)
        try:
            return self.s3.Object(self.bucket, key).get()["Body"].read()
        except botocore.exceptions.ClientError:
            return None

    def put(self, key1, val1):
        key = self._mapkey(key1)
        self.s3.Bucket(self.bucket).put_object(Key=key, Body=val1)

    def check(self, key1):
        key = self._mapkey(key1)
        try:
            self.s3.Object(self.bucket, key).load()
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                return False
            else:
                raise
        else:
            return True

    def delete(self, key1):
        key = self._mapkey(key1)
        try:
            self.s3.Bucket(self.bucket).delete_objects(Delete={"Objects":[{"Key":key}]})
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

    ds = DataStore_S3("test.s3-", Hash_f)
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
