#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import asyncio
import shlex
import json
from . import compiler

class Hook(object):
    def __init__(self, cls, methodname, wrapper, decorator=None):
        """
        wrapper: wrapper function with first arg as old imp
        """
        self.hook_cls = cls
        self.hook_methodname = methodname
        self.hook_wrapper = wrapper
        self.hooked = False
        self.decorator = decorator

    def hook(self):
        if not self.hooked:
            old = getattr(self.hook_cls, self.hook_methodname)
            self.hook_old = old
            wrapper = self.hook_wrapper
            def newimp(*args, **params):
                return wrapper(old, *args, **params)
            if self.decorator: newimp = self.decorator(newimp)
            setattr(self.hook_cls, self.hook_methodname, newimp)
            self.hook_new = newimp

    def unhook(self):
        if self.hooked:
            assert getattr(self.hook_cls, self.hook_methodname) == self.hook_new, "the method should be the hook"
            setattr(self.hook_cls, self.hook_methodname, self.hook_old)

    def __enter__(self):
        self.hook()

    def __exit__(self, *exc):
        self.unhook()


class Compiler(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.request = []
        async def request(old, *args, **params):
            cls.request.append( (args, params) )

        cls.hook = Hook(compiler.SourceKitten, "request", request, staticmethod)
        cls.hook.hook()

    @classmethod
    def tearDownClass(cls):
        cls.hook.unhook()

    def test_xcodelog(self):
        # test data
        log = """
            other cmds
            /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/swiftc -module-name Hello a.swift b.swift c\ c.swift "d d.swift"
            other cmds
            apple/swiftc -module-name World e.swift f.swift
        """
        lines = log.splitlines()
        args =  shlex.split(lines[2])
        args2 = shlex.split(lines[4])
        def swift_files(args):
            return {i for i in args if i.endswith(".swift")}
        compile_files = swift_files(args) | swift_files(args2)

        # begin
        c = compiler.Compiler.from_xcode_log(log, cache_dir="/tmp/test" , overwrite=True)

        async def hookIndex(old, *args, **params):
            out = params.get("out")
            if out: self.assertFalse( out.closed )
            err = params.get("err")
            if err: self.assertFalse( err.closed )

            await old(*args, **params)
        with Hook(compiler.SourceKitten, "index", hookIndex, staticmethod):
            asyncio.get_event_loop().run_until_complete(c.index())

        # assert
        self.assertEqual(len(asyncio.Task.all_tasks()), 0)
        self.assertEqual(len(self.request), len(compile_files))
        self.assertSetEqual(
            {r[0][1]["key.name"] for r in self.request},
            compile_files
        )
        self.assertSetEqual(
            {" ".join(r[0][1]["key.compilerargs"]) for r in self.request},
            {" ".join(args[1:])} | {" ".join(args2[1:])}
        )
        self.request.clear()

        # without overwrite, request nothing after write
        c = compiler.Compiler.from_xcode_log(log, cache_dir="/tmp/test" , overwrite=False)
        asyncio.get_event_loop().run_until_complete(c.index())

        self.assertEqual(len(asyncio.Task.all_tasks()), 0)
        self.assertEqual(len(self.request), 0)



class SourceKitten(unittest.TestCase):
    def test_request(self):
        async def run():
            o, e = await compiler.SourceKitten.request('source.request.protocol_version')
            self.assertTrue(not e)
            o = json.loads(o)
            self.assertTrue( "key.version_major" in o )
        asyncio.get_event_loop().run_until_complete(
            asyncio.gather( *(run() for i in range(10)) )
        )

if __name__ == "__main__":
    # from importlib import reload
    # reload(compiler)
    unittest.main()
