#!/usr/bin/env python
# encoding: utf-8

import os, sys, argparse, re

def parse():
    parser = argparse.ArgumentParser(description = 'convert line ending between unix and dos')
    parser.add_argument('files', nargs = '+', help= "file will be convert")
    parser.add_argument('-s', '--suffix', help = 'out suffix, default will be overwrite', default='')
    parser.add_argument('-d', '--dos', help = 'the file end type, if false, convert dos to unix, else convert to dos', action='store_true')
    return parser.parse_args()

def main():
    args = parse()
    suffix = args.suffix #!! suffix = ""
    for f in args.files:
        try:
            print ("read", f)
            with open(f, "rb") as af:
                s = af.read() #!! s = ""
            if args.dos:
                pass # TODO
            else:
                ns = s.replace(b"\r\n", b"\n")
                if ns != s:
                    f = f+suffix
                    print ("write", f)
                    with open(f, 'wb') as af:
                        af.write(ns)
        except Exception as e:
            print (f, e.message)

if __name__ == '__main__':
    main()
