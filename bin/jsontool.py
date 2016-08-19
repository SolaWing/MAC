#!/usr/bin/env python
# encoding: utf-8

import sys
import json

def toUtf8IfNeed(s):
    if (isinstance(s, unicode)):
        s = s.encode('utf-8')
    return s

def main():
    if len(sys.argv) == 1:
        infile = sys.stdin
        outfile = sys.stdout
    elif len(sys.argv) == 2:
        infile = open(sys.argv[1], 'rb')
        outfile = sys.stdout
    elif len(sys.argv) == 3:
        infile = open(sys.argv[1], 'rb')
        outfile = open(sys.argv[2], 'wb')
    else:
        raise SystemExit(sys.argv[0] + " [infile [outfile]]")
    with infile:
        try:
            obj = json.load(infile, "utf-8") 
        except ValueError, e:
            raise SystemExit(e)
    with outfile:
        s = json.dumps(obj,  sort_keys=False, ensure_ascii=False,
                  indent=4, separators=(',', ': '))
        outfile.write(toUtf8IfNeed(s))
        outfile.write('\n')


if __name__ == '__main__':
    main()

