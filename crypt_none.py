#!/usr/bin/env python3

from crypt_base import Crypt

class Crypt_none(Crypt):
    def __init__(self, key1):
        super().__init__()
    
    def encrypt(self, s):
        return s
    
    def decrypt(self, s):
        return s

if __name__ == "__main__":
    c = Crypt_none(None)
    en = c.encrypt(b"a")
    de = c.decrypt(en)
    print(de)
    assert(de == b"a")
