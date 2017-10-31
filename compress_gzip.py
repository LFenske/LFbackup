#!/usr/bin/env python3

from compress_base import Compress

import gzip

class Compress_Gzip(Compress):

    compresslevel = 9

    def __init__(self):
        super().__init__()

    def compress(self, s):
        return gzip.  compress(s, compresslevel=self.compresslevel)

    def decompress(self, s):
        return gzip.decompress(s)

if __name__ == "__main__":
    c = Compress_Gzip()
    s = b"abcdefghijklmnopqrstuvwxyz"
    en = c.  compress(s)
    de = c.decompress(en)
    print(de)
    assert(de == s)
