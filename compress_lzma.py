#!/usr/bin/env python3

from compress_base import Compress

import lzma


class Compress_Lzma(Compress):

    def __init__(self):
        super().__init__()

    def compress(self, s):
        return lzma.  compress(s)

    def decompress(self, s):
        return lzma.decompress(s)

if __name__ == "__main__":
    c = Compress_Lzma()
    s = b"abcdefghijklmnopqrstuvwxyz"
    en = c.  compress(s)
    de = c.decompress(en)
    print(de)
    assert(de == s)
    en2= c.  compress(s)
    assert(en == en2)
