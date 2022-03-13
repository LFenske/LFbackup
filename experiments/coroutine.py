#!/usr/bin/env python3

def coroutine(func):
    def start(*args,**kwargs):
        cr = func(*args,**kwargs)
        next(cr)
        return cr
    return start

@coroutine
def grep(pattern, target):
    print("Looking for %s" % pattern)
    try:
        while True:
            line = (yield)
            if pattern in line:
                target.send(line)
    except GeneratorExit:
        print("Going away.  Goodbye.")

@coroutine
def printer():
    while True:
        line = (yield)
        print(line, end=' ')

import time
def follow(thefile, target):
    thefile.seek(0,2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue
        target.send(line)

f = open("/tmp/access-log")
follow(f,
       grep('python',
            printer()))
