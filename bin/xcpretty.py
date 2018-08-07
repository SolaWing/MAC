#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re, os, sys
import shlex

def echo(s):
    print(s, file=sys.stderr)

compileSwiftModule = re.compile(r"""
    ^CompileSwiftSources\s*
""", re.X)
compileSwift = re.compile(r"""^CompileSwift\s+
                          \w+\s+ # normal
                          \w+\s+ # x86_64
                          (.+)$""", # file
                          re.X)
def readUntilEmptyLine(i):
    li = []
    while True:
        line = next(i).strip()
        if not line: return li
        li.append(line)

cacheDir = None

# def readFileList(path):
#     with open(path) as f:
#         return f.read().splitlines()

def extractSwiftCompileCommandFromSwiftC(command, directory=None):
    from subprocess import Popen, PIPE, STDOUT
    import json

    sp = Popen(command, shell=True, stdout=PIPE, stderr=STDOUT, cwd=directory)
    items = []

    if cacheDir is None:
        # no cacheDir, don't replace filelist
        _copyFileList = lambda p: p
    else:
        # copy swiftc temp filelist
        import shutil
        copyed = set()
        def _copyFileList(op):
            np = os.path.join(cacheDir, os.path.basename(op))
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
        line = sp.stdout.readline() # type: bytes
        if not line:
            break # EOF

        n = int(line) # ignore line non begin with a size number
        if n <= 0: continue

        jsondata = sp.stdout.read(n)
        info = json.loads(jsondata) # type: dict

        cmd = info["command"]
        cmdArgs = shlex.split(cmd)
        if not cmdArgs[0].endswith("swift"): continue

        primaryIndex = cmdArgs.index("-primary-file") + 1
        primaryFile  = cmdArgs[primaryIndex]

        def mayReplaceFileList(cmdArgs):
            try: # replace filelist
                fileListIndex = cmdArgs.index("-filelist") + 1
                saveListPath      = _copyFileList(cmdArgs[fileListIndex]) # type: list
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

    def parseCompileSwiftModule(self, line):
        m = compileSwiftModule.match(line)
        if not m: return

        li = readUntilEmptyLine(self._input)
        if not li: return

        command = li[-1] # type: str
        if "bin/swiftc " not in command:
            echo("Error: ================= Can't found swiftc\n" + command)
            return

        # module = {}
        directory = next( (i[len("cd "):] for i in li if i.startswith("cd ")), None )
        # if directory: module["directory"] = directory

        # 这个命令可以运行获得一堆命令, 输出到Stderr, 如果吐出-filelist, 结束时就会删除
        ## 如果自己组装, 需要把里面的参数全部拆开
        # 还是直接运行吧
        echo("CompileSwiftSources")
        return extractSwiftCompileCommandFromSwiftC(command, directory)

    def parseCompileSwift(self, line):
        m = compileSwift.match(line)
        if not m: return

        echo(f"CompileSwift {m.group(1)}")
        li = readUntilEmptyLine(self._input)
        if not li: return

        item = {"file": m.group(1), "command": li[-1]}
        for line in li:
            if line.startswith("cd "):
                item["directory"] = line[len("cd "):]
                break
        return item

    def parse(self):
        items = []

        matcher = [
            self.parseCompileSwiftModule,
            # self.parseCompileSwift,
        ]
        try:
            while True:
                line = next(self._input) # type: str

                if line.startswith("==="): echo(line); continue
                for m in matcher:
                    item = m(line)
                    if item:
                        if isinstance(item, dict): items.append(item)
                        else: items.extend(item)
                        break
        except StopIteration:
            return items

def dump_jsonDataBase(items, output):
    import json
    json.dump(items, output, ensure_ascii=False, check_circular=False)

def main():
    import argparse
    parser = argparse.ArgumentParser(description="pass xcodebuild output log, use stderr as log")
    parser.add_argument("input", nargs="?", default="-", help="input file, default will use stdin")
    parser.add_argument("-o", "--output", default="-", help="output file, default will be stdout" )
    a = parser.parse_args()

    if a.input == "-": a.input = sys.stdin
    else: a.input = open(a.input, "r")
    if a.output == "-": a.output = sys.stdout
    else:
        global cacheDir;
        cacheDir = os.path.join( os.path.dirname(os.path.abspath(a.output)), os.path.basename(a.output) + "cache")
        os.makedirs(cacheDir, exist_ok=True)
        a.output = open(a.output, "w")

    items = XcodeLogParser(a.input, echo).parse()
    dump_jsonDataBase(items, a.output)

if __name__ == "__main__":
    main()
