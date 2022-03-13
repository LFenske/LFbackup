#!/usr/bin/env python3

import gzip

from coroutine_decorator import *
from buffer import Buffer

class Compress_Gzip(object):

    @decorator.coroutine
    def compress(pipe):
        buffer = Buffer()
        gzipper = gzip.GzipFile(None, mode='wb', fileobj=buffer)
        while True:
            try:
                datain = yield
            except GeneratorExit:
                # preceding task in pipe is done and closed us
                break
            gzipper.write(datain)   # send the received data to gzip
            dataout = buffer.read() # pull out whatever results we have so far
            pipe.send(dataout)      # push it through the pipe

        gzipper.close()          # we're all done now, let gzip finalize
        dataout = buffer.read()
        pipe.send(dataout)
        pipe.close()             # tell downstream that we're done

