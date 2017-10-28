#!/usr/bin/env python3

import hashlib
from hash_base import Hash

class Hash_SHA1(Hash):
    def __init__(self):
        super().__init__()
        self.hashmethod = hashlib.sha1()

    def hashlen(self):
        return 20

    def update(self, s):
        self.hashmethod.update(s)

    def digest(self):
        return self.hashmethod.digest()

if __name__ == "__main__":
    h = Hash_SHA1()
    h.update(b"a")
    print(h.hexdigest())
    assert(h.hexdigest() == "86f7e437faa5a7fce15d1ddcb9eaeaea377667b8")

    h = Hash_SHA1()
    h.update(b"c")
    h.update(b"def")
    print(h.hexdigest())
    assert(h.hexdigest() == "25bf58983b8ab103fa88b4032503fc8b65651ca1")
