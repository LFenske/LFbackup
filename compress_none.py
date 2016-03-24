#!/usr/bin/env python3

from compress_base import Compress

class Compress_none(Compress):
    def __init__(self):
        super().__init__()
    
    def compress(self, s):
        return s
    
    def decompress(self, s):
        return s

if __name__ == "__main__":
    c = Compress_none()
    en = c.  compress(b"a")
    de = c.decompress(en)
    assert(de == b"a")