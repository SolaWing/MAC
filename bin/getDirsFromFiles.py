#!/usr/bin/env python
# encoding: utf-8

import argparse,os,sys

def parse():
    parser = argparse.ArgumentParser(description = "out dirs from files")
    parser.add_argument('files', nargs = '*', help = 'input files, if not specify, use stdin instead')
    return parser.parse_args()

def main():
    args = parse()
    if not args.files:
        args.files = sys.stdin;
    dirs = {os.path.dirname(f) for f in args.files}
    for d in dirs: print d;

if __name__ == '__main__':
    main()
