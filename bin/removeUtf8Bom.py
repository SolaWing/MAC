#!/usr/bin/env python
# encoding: utf-8

import os, argparse

def parse():
    parser = argparse.ArgumentParser(description = "remove file format bom")
    parser.add_argument("file", nargs = "+")
    return parser.parse_args()

def main():
    args = parse()
    for f in args.file:
        if os.path.isfile(f):
            with open(f, "rb") as fin:
                s = fin.read(3)
                if s != b"\xef\xbb\xbf":
                    print "continue"
                    continue
                s = fin.read()
            with open(f, "wb") as fout:
                fout.write(s)

if __name__ == '__main__':
    main()

