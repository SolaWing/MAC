#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re, os, sys
import shlex

def echo(s):
    print(s, file=sys.stderr)

compile_swift_module = re.compile(r"""
    ^CompileSwiftSources\s*
""", re.X)
compile_swift = re.compile(r"""^CompileSwift\s+
                          \w+\s+ # normal
                          \w+\s+ # x86_64
                          (.+)$""", # file
                          re.X)
cmd_split_pattern = re.compile(r"""
"([^"]*)" |     # like "xxx xxx"
'([^']*)' |     # like 'xxx xxx'
((?:\\[ ]|\S)+) # like xxx\ xxx
""", re.X)
def cmd_split(s):
    # shlex.split is slow, use a simple version, only consider most case
    return [m.group(m.lastindex)
            for m in cmd_split_pattern.finditer(s)]

def read_until_empty_line(i):
    li = []
    while True:
        line = next(i).strip()
        if not line: return li
        li.append(line)

def extract_swift_files_from_swiftc(command):
    return [a for a in cmd_split(command) if a.endswith(".swift")]

cache_dir = None
async def extract_compile_command_from_swiftc(command, directory=None):
    # from subprocess import Popen, PIPE, STDOUT
    from asyncio.subprocess import create_subprocess_shell, PIPE, STDOUT
    import json

    # sp = Popen(command, shell=True, stdout=PIPE, stderr=STDOUT, cwd=directory)
    sp = await create_subprocess_shell(command, stdout=PIPE, stderr=STDOUT, cwd=directory)
    items = []

    if cache_dir is None:
        # no cache_dir, don't replace filelist
        _copy_filelist = lambda p: p
    else:
        # copy swiftc temp filelist
        import shutil
        copyed = set()
        def _copy_filelist(op):
            np = os.path.join(cache_dir, os.path.basename(op))
            if op in copyed: return np
            if os.path.exists(op):
                shutil.copy2(op, np)
                copyed.add(op)
                return np
            else:
                echo(f"unexist filelist path: {op}")
            return op

    while True:
      try:
        # swiftc may echo a filelist, and delete it when end. so need to save the filelist when it's alive and can't read all..
        line = await sp.stdout.readline() # type: bytes
        if not line:
            break # EOF

        n = int(line) # ignore line non begin with a size number
        if n <= 0: continue

        # read(n)可能没读取n这么多字节
        jsondata = await sp.stdout.readexactly(n)
        info = json.loads(jsondata) # type: dict

        cmd = info["command"]
        cmdArgs = cmd_split(cmd)
        if not cmdArgs[0].endswith("swift"): continue

        primaryIndex = cmdArgs.index("-primary-file") + 1
        primaryFile  = cmdArgs[primaryIndex]

        def mayReplaceFileList(cmdArgs):
            try: # replace filelist
                fileListIndex = cmdArgs.index("-filelist") + 1
                saveListPath      = _copy_filelist(cmdArgs[fileListIndex]) # type: list
                cmdArgs[fileListIndex] = saveListPath
            except ValueError:
                pass
            except Exception as e:
                import traceback
                traceback.print_exc()
        mayReplaceFileList(cmdArgs)

        item = {};
        item["file"] = primaryFile
        if directory: item["directory"] = directory
        item["command"] = " ".join(map(shlex.quote, cmdArgs))
        items.append(item)
        echo("compile " + primaryFile)

      except (KeyError, ValueError) as e: # info load exception, ignore no cmd, no primaryFile
          pass
      except Exception as e: # file load exception
          import traceback
          traceback.print_exc()
    return items

class XcodeLogParser(object):
    def __init__(self, _input, _logFunc):
        self._input = _input
        self._log = _logFunc

    def parse_compile_swift_module(self, line):
        m = compile_swift_module.match(line)
        if not m: return

        li = read_until_empty_line(self._input)
        if not li: return

        command = li[-1] # type: str
        if "bin/swiftc " not in command:
            echo("Error: ================= Can't found swiftc\n" + command)
            return

        module = {}
        directory = next( (i[len("cd "):] for i in li if i.startswith("cd ")), None )
        if directory: module["directory"] = directory
        module["command"] = command
        module["files"] = extract_swift_files_from_swiftc(command)
        return module

        # 这个命令可以运行获得一堆命令, 输出到Stderr, 如果吐出-filelist, 结束时就会删除
        ## 如果自己组装, 需要把里面的参数全部拆开
        # 还是直接运行吧
        # return extract_compile_command_from_swiftc(command, directory)

    def parse_compile_swift(self, line):
        m = compile_swift.match(line)
        if not m: return

        echo(f"CompileSwift {m.group(1)}")
        li = read_until_empty_line(self._input)
        if not li: return

        item = {"file": m.group(1), "command": li[-1]}
        for line in li:
            if line.startswith("cd "):
                item["directory"] = line[len("cd "):]
                break
        return item

    def parse(self):
        from inspect import iscoroutine
        import asyncio
        items = []
        futures = []
        def append(item):
            if isinstance(item, dict): items.append(item)
            else: items.extend(item)

        matcher = [
            self.parse_compile_swift_module,
            # self.parse_compile_swift,
        ]
        try:
            while True:
                line = next(self._input) # type: str

                if line.startswith("==="): echo(line); continue
                for m in matcher:
                    item = m(line)
                    if item:
                        if iscoroutine(item):
                            futures.append( item )
                        else: append(item)
                        break
        except StopIteration:
            pass

        if len(futures) > 0:
            echo("waiting... ")
            for item in asyncio.get_event_loop().run_until_complete( asyncio.gather(*futures) ):
                append(item)

        return items

def dump_database(items, output):
    import json
    # pretty print, easy to read with editor. compact save little size. only about 0.2%
    json.dump(items, output, ensure_ascii=False, check_circular=False, indent="\t")

def merge_database(items, database_path):
    import json
    # 根据ident(file属性)，增量覆盖更新
    def identifier(item):
        if isinstance(item, dict):
            return item.get("file")
        return None # other type info without identifier simplely append into file

    with open(database_path, "r+") as f:
        # try best effort to keep old data
        old_items = json.load(f)

        new_file_map = {}
        for item in items:
            ident = identifier(item)
            if ident: new_file_map[ident] = item

        dealed = set()
        def get_new_item(old_item):
            if isinstance(old_item, dict):
                ident = identifier(old_item)
                if ident:
                    dealed.add(ident)

                    new_item = new_file_map.get(ident)
                    if new_item: return new_item
            return old_item

        final = [get_new_item(item) for item in old_items]
        final.extend( item for item in items if identifier(item) not in dealed )

        f.seek(0)
        dump_database(final, f)
        f.truncate()

def main():
    import argparse
    parser = argparse.ArgumentParser(description="pass xcodebuild output log, use stderr as log")
    parser.add_argument("input", nargs="?", default="-", help="input file, default will use stdin")
    parser.add_argument("-o", "--output", default="-", help="output file, default will be stdout" )
    parser.add_argument("-a", "--append", action="store_true", help="append to output file instead of replace. same item will be overwrite" )
    a = parser.parse_args()

    if a.input == "-": in_fd = sys.stdin
    else: in_fd = open(a.input, "r")
    if a.output == "-": get_out_fd = lambda: sys.stdout
    else:
        global cache_dir;
        cache_dir = os.path.join( os.path.dirname(os.path.abspath(a.output)), os.path.basename(a.output) + "cache")
        os.makedirs(cache_dir, exist_ok=True)
        get_out_fd = lambda: open(a.output, "w") # open will clear file

    items = XcodeLogParser(in_fd, echo).parse()
    if a.append and os.path.exists(a.output):
        merge_database(items, a.output)
    else:
        dump_database(items, get_out_fd())

if __name__ == "__main__":
    main()
