#!/usr/bin/env python3

import re, os, sys

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
splitBySpaces = re.compile(r"(?:\\ |\S)+")

def readUntilEmptyLine(i):
    li = []
    while True:
        line = next(i).strip()
        if not line: return li
        li.append(line)

def parseCompileSwiftModule(line, i):
    m = compileSwiftModule.match(line)
    if not m: return

    li = readUntilEmptyLine(i)
    if not li: return

    item = {}
    directory = next( (i[len("cd "):] for i in li if i.startswith("cd ")), None )
    if directory: item["directory"] = directory

    command = iter(splitBySpaces(li[-1])) # type: list
    args = []
    try:
        while True:
            #  TODO: 这个命令可以运行获得一堆命令
            # 如果自己组装, 需要把里面的参数全部拆开
            a = next(command)
            if a == "-module-name":
                item["modulename"] = next(command)
                continue
    except StopIteration:
        pass

def parseCompileSwift(line, i):
    m = compileSwift.match(line)
    if not m: return

    echo(f"CompileSwift {m.group(1)}")
    li = readUntilEmptyLine(i)
    if not li: return

    item = {"file": m.group(1), "command": li[-1]}
    for line in li:
        if line.startswith("cd "):
            item["directory"] = line[len("cd "):]
            break
    return item

def parse(i):
    items = []

    matcher = [
        # parseCompileSwiftModule,
        parseCompileSwift,
    ]
    try:
        while True:
            line = next(i) # type: str

            if line.startswith("==="): echo(line); continue
            for m in matcher:
                item = m(line, i)
                if item:
                    items.append(item)
                    break
    except StopIteration:
        return items

def dump_jsonDataBase(items, output):
    import json
    json.dump(items, output, ensure_ascii=False, check_circular=False)

def main():
    import argparse
    parser = argparse.ArgumentParser(description="pass xcodebuild output log")
    parser.add_argument("input", nargs="?", default="-", help="input file, default will use stdin")
    parser.add_argument("-o", "--output", default="-", help="output file, default will be stdout" )
    a = parser.parse_args()

    if a.input == "-": a.input = sys.stdin
    else: a.input = open(a.input, "r")
    if a.output == "-": a.output = sys.stdout
    else: a.output = open(a.output, "w")
    items = parse(a.input)
    dump_jsonDataBase(items, a.output)

if __name__ == "__main__":
    main()
