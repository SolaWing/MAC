#!/usr/bin/env python
# encoding: utf-8

import sys
import json
import codecs

def main():
    if len(sys.argv) == 1:
        infile = sys.stdin
        if "b" in infile.mode:
            infile = codecs.getreader("utf-8")(infile)
        outfile = sys.stdout
        if "b" in outfile.mode:
            outfile = codecs.getwriter('utf-8')(outfile)
    elif len(sys.argv) == 2:
        infile = open(sys.argv[1], 'rb')
        infile = codecs.getreader("utf-8")(infile)
        outfile = sys.stdout
        if "b" in outfile.mode:
            outfile = codecs.getwriter('utf-8')(outfile)
    elif len(sys.argv) == 3:
        infile = open(sys.argv[1], 'rb')
        infile = codecs.getreader("utf-8")(infile)
        outfile = open(sys.argv[2], 'wb')
        outfile = codecs.getwriter('utf-8')(outfile)
    else:
        raise SystemExit(sys.argv[0] + " [infile [outfile]]")
    with infile:
        try:
            obj = json.load(infile)
        except ValueError as e:
            raise SystemExit(e)
    with outfile:
        s = json.dumps(obj,  sort_keys=False, ensure_ascii=False,
                  indent=4, separators=(',', ': '))
        outfile.write(s)
        outfile.write('\n')


if __name__ == '__main__':
    main()

