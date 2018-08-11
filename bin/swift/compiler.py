import sys, re, os
import logging
import functools
import shlex
import json, tempfile
from hashlib import md5

from asyncio import subprocess as process, coroutine
from .tool import LazyProperty, AsyncExecutor, echo, strong_style as strong


SOURCE_KITTEN = "sourcekitten"
LOG = logging.getLogger(__name__)

class SourceKitten(object):
    @staticmethod
    async def request(method, params = {}, out=process.PIPE, err=process.PIPE):
        """
        :param file out: should be a bytes file-like
        """
        request = json.dumps(params, ensure_ascii=False)
        request = "{key.request: " + method + "," + request[1:] # sourcekitten yaml request must not encapsulate by ""

        with tempfile.NamedTemporaryFile(delete=True) as yaml:
            yaml.write(request.encode())
            yaml.flush()
            filename = yaml.name
            p = await process.create_subprocess_exec(
                SOURCE_KITTEN, 'request', '--yaml', filename,
                stdout=out,
                stderr=err,
            ) # type: process.Process
            o,e = await p.communicate()
            if e: LOG.error("request error: %s", e)

        return (o, e)

    @staticmethod
    async def index(swift_file, compilerargs, **config):
        assert swift_file
        assert compilerargs
        return await SourceKitten.request("source.request.indexsource", {
            "key.name": swift_file,
            "key.sourcefile": swift_file,
            "key.compilerargs": compilerargs
        }, **config)

class Compiler(object):
    class Module(object):
        def __init__(self, name, cmd):
            """
            :param str name: module name
            :param str cmd: swiftc compile args
            """
            self.name = name
            self.args = shlex.split(cmd)

        @LazyProperty
        def files(self):
            return [f for f in self.args if f.endswith(".swift")]

        @LazyProperty
        def sourcekitten_args(self):
            def generate():
                it = iter(self.args)
                try:
                    next(it) # skip swiftc
                    while True:
                        i = next(it)
                        if i in {"-incremental", "-parseable-output"}: continue
                        if i in {"-output-file-map"}: next(it); continue
                        yield i
                except StopIteration as e: pass

            return [i for i in generate()]

    @staticmethod
    def from_xcode_log(build_log, **params):
        matches = [ (m.group(1), m.group(2)) for m in re.finditer(
            r'^\s*([\w/ -.]*swiftc.*-module-name (\w+).*)',
            build_log, re.M) ]

        cmds, modules = zip(*matches)

        return Compiler(cmds, module_names=modules, **params)

    def __init__(self, cmds, cache_dir = None, overwrite = False, module_names = None):
        """
        :param list cmds: [cmd]
        :param list module_names: corresponding module name of cmds
        """
        if module_names is None:
            #  TODO:  <09-08-18, yourname> # support no pass module_names
            pass
        self.modules = {name: self.Module(name, cmd) for name, cmd in zip( module_names, cmds)}

        if cache_dir is None:
            cache_dir = os.path.join(tempfile.tempdir, "SwiftCache")
        self.cache_dir = cache_dir
        self.overwrite = overwrite

    async def index(self, modules = None):
        """index modules find in cmd"""
        self.check_dependency()
        # one thread must have only one event loop, other af may get it and use it. like wait, queue, etc..
        import asyncio
        if modules is None: modules = self.modules.keys()
        indexModuels = filter(None, (self.modules.get(m) for m in modules))

        loop = asyncio.get_event_loop()
        i = 0
        async with AsyncExecutor(maxworkers=4, loop=loop) as queue:
            for m in indexModuels: # type: Compiler.Module
                for index_file in self._index_moduel(m):
                    await queue.put(index_file)
                    i+= 1

    def _index_moduel(self, module):
        """
        return iter of coroutine for index file
        """
        dir_path = os.path.join(self.cache_dir, module.name)
        os.makedirs(dir_path, exist_ok=True)
        compilerargs = module.sourcekitten_args

        LOG.debug(f"index module {module.name} with args: {compilerargs}")
        # use yield to show log when really run
        yield coroutine(echo)(f"index module {strong(module.name)}")
        for filepath in module.files:
            async def run(filepath):
                path_hash = md5(filepath.encode()).hexdigest()
                output_path = os.path.join(dir_path, f"swift_{path_hash}_{os.path.basename(filepath)}")
                if not self.overwrite and os.path.exists(output_path): return
                with open(output_path, "wb") as output_file:
                    echo(f"index {strong(filepath)} to {output_path}")
                    # file should wait work complete
                    await SourceKitten.index(filepath, compilerargs, out=output_file)
            yield run(filepath) # delay execute, need to capture by value

    @staticmethod
    def check_dependency():
        import shutil
        if not shutil.which(SOURCE_KITTEN):
            raise FileNotFoundError(SOURCE_KITTEN)
