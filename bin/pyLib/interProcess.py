#!/usr/bin/env python
# encoding: utf-8

import os
try:
    import fcntl
    import errno
except ImportError:
    fcntl = None

class File(file):
        
    def acquire(self, blocking=True):
        if fcntl:
            if blocking:
                fcntl.flock(self, fcntl.LOCK_EX)
            else:
                try:
                    fcntl.flock(self, fcntl.LOCK_EX|fcntl.LOCK_NB)
                except IOError, e:
                    if e.errno == errno.EWOULDBLOCK:
                        return False
                    raise e
        return True

    def release(self):
        if fcntl:
            fcntl.flock(self, fcntl.LOCK_UN)

    def __enter__(self):
        super().__enter__()
        self.acquire()


    def __exit__(self, *args):
        self.release()
        return super().__exit__(*args)

class RLock(object):
    def __init__(self, name):
        self.name = name
        if fcntl:
            self.handle = open('/tmp/'+name, 'w')

    def acquire(self, blocking=True):
        if fcntl:
            if blocking:
                fcntl.flock(self.handle, fcntl.LOCK_EX)
            else:
                try:
                    fcntl.flock(self.handle, fcntl.LOCK_EX|fcntl.LOCK_NB)
                except IOError, e:
                    if e.errno == errno.EWOULDBLOCK:
                        return False
                    raise e
        return True

    def release(self):
        if fcntl:
            fcntl.flock(self.handle, fcntl.LOCK_UN)

    __enter__ = acquire

    def __exit__(self, *args):
        self.release()

    def __del__(self):
        if fcntl:
            self.handle.close()
