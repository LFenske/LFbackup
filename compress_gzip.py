#!/usr/bin/env python3

from compress_base import Compress

import gzip
import io


class Compress_Gzip(Compress):

    compresslevel = 9

    def __init__(self):
        super().__init__()

    def compress(self, s):
#        return gzip.  compress(s, compresslevel=self.compresslevel, mtime=0)
        buf = io.BytesIO()
        with gzip.GzipFile(fileobj=buf, mode='wb', mtime=0) as fd:
            fd.write(s)
        return buf.getvalue()

    def decompress(self, s):
        return gzip.decompress(s)

if __name__ == "__main__":
    c = Compress_Gzip()
    s = b"abcdefghijklmnopqrstuvwxyz"
    en = c.  compress(s)
    de = c.decompress(en)
    print(de)
    assert(de == s)
    import time
    time.sleep(1)
    en2= c.  compress(s)
    assert(en == en2)
