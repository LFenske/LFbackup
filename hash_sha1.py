#!/usr/bin/env python3

import hashlib
from hash_base import Hash

class Hash_sha1(Hash):
    def __init__(self):
        super().__init__()
        self.hashmethod = hashlib.sha1()
    
    def update(self, s):
        self.hashmethod.update(s)
    
    def digest(self):
        return self.hashmethod.digest()

    def hexdigest(self):
        return self.hashmethod.hexdigest()

if __name__ == "__main__":
    h = Hash_sha1()
    h.update(b"a")
    print(h.hexdigest())