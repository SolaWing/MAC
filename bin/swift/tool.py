#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from asyncio import Queue, AbstractEventLoop, coroutine
from functools import partial

# can change to other handler
handler = partial(print, file=sys.stderr)
def echo(*messages):
    handler(*messages)

def strong_style(message):
    return f"\033[31;1m{message}\033[0m"

class LazyProperty(object):
    """lazy property"""
    def __init__(self, getter):
        self._getter = getter

    def __get__(self, i, cls):
        r = self._getter(i)
        i.__setattr__(self._getter.__name__, r)
        return r

class AsyncExecutor(object):
    """
    create a executor context, with maxworkers, get task(awaitable) from queue
    queue default to Queue.
    with context will return queue to add task
    async with will wait for queue complete
    """

    default_worker_count = 4
    def __init__(self, queue = None, maxworkers=0, loop=None):
        """
        :param AbstractEventLoop loop: worker runloop
        """
        if queue is None:
            if maxworkers <= 0: maxworkers = self.default_worker_count
            queue = Queue(maxworkers, loop=loop)
        self.queue = queue

        if maxworkers <= 0:
            maxworkers = queue.maxsize if queue.maxsize > 0 else self.default_worker_count
        self.maxworkers = maxworkers

        if loop is None: loop = queue._loop
        self.loop = loop

        self.tasks = []

    @property
    def running(self):
        return len(self.tasks) > 0

    def start(self):
        if self.running: return
        self.tasks = [self.loop.create_task(worker(self.queue)) for i in range(self.maxworkers)]

    def cancel(self):
        for item in self.tasks:
            item.cancel()
        self.tasks = []

    async def wait(self):
        return await self.queue.join()

    def __enter__(self):
        self.start()
        return self.queue

    __aenter__ = coroutine(__enter__)

    def __exit__(self, *exc):
        self.cancel()
        return False

    async def __aexit__(self, *exc):
        await self.queue.join()
        self.cancel()
        return False

async def worker(queue):
    """
    task queue worker, queue's element must be awaitable. after awaitable return, mark complete
    if the task has return value, wrap it as a future, and get value from it
    :param Queue queue: get task from queue
    """
    while True:
        task = await queue.get()
        try:
            await task
            # exception怎么处理没想好..
        finally:
            # exception also need to mark done, so join can complete
            queue.task_done()
