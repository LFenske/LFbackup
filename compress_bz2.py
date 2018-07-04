#!/usr/bin/env python3

from compress_base import Compress

import bz2


class Compress_Bz2(Compress):

    compresslevel = 9

    def __init__(self):
        super().__init__()

    def compress(self, s):
        return bz2.  compress(s, compresslevel=self.compresslevel)

    def decompress(self, s):
        return bz2.decompress(s)

if __name__ == "__main__":
    c = Compress_Bz2()
    s = b"abcdefghijklmnopqrstuvwxyz"
    en = c.  compress(s)
    de = c.decompress(en)
    print(de)
    assert(de == s)
    en2= c.  compress(s)
    assert(en == en2)
