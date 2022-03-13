#!/usr/bin/env python3

from coroutine_decorator import *

chunksize = 1024

def file_reader(name, pipe):
    with open(name, "rb") as fd:
        while True:
            dat = fd.read(chunksize)
            if not dat:
                break
            pipe.send(dat)
    pipe.close()

@decorator.coroutine
def file_writer(name):
    with open(name, "wb") as fd:
        while True:
            try:
                dat = yield
                fd.write(dat)
            except GeneratorExit:
                break

