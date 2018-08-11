#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
generate attribute wrapper function.  eg:
Bold("aaa") will gen a bold string used in terminal

can also use attr to generate term string. eg:
attr("aaa", Bold, Red)
"""

# [终端样式表](https://en.wikipedia.org/wiki/ANSI_escape_code#Colors)
import re

def make():
    """
    export dynamic names to global scope
    """
    def _makeAttr(name, val):
        def fun(s):
            return attr(s, fun)
        fun.val = val
        fun.name = name
        globals()[name] = fun

    attrs = {
        0 : ('Clear', 'Bold', 'Shallow', 'Italic', 'Underline'),
        3 : ('Black', 'Red', 'Green', 'Yellow', 'Blue', 'Magenta', 'Cyan', 'White'),
        4 : ('BGBlack', 'BGRed', 'BGGreen', 'BGYellow', 'BGBlue', 'BGMagenta', 'BGCyan', 'BGWhite'),
    }

    for base, tup in attrs.items():
        for i, name in enumerate(tup):
            _makeAttr(name, base*10+i)

make()
del make

def attr(s, *attributes):
    """
    add terminal attributes surround s, and return it
    if attributes is Clear, remove attribute in s
    :type s: str
    """
    if len(attributes) == 0: return s # do nothing if not pass attr
    if attributes[0].val == 0:
        attributes = attributes[1:]
        should_clear = True
    else:
        should_clear = False


    attr_pattern = "\x1b\\[(\\d+(?:;\\d+)*)m"

    prefix = re.match(attr_pattern, s)
    if prefix:
        s = s[prefix.end(0):] # remove prefix, re add later
    if should_clear or not prefix:
        prefix = set()
    else:
        prefix = set(prefix.group(1).split(';')) # old style

    postfix = re.search(attr_pattern, s)
    if postfix:
        s = s[:postfix.start(0)] # remove postfix
    postfix = "\x1b[0m" # reset style

    for a in attributes:
        prefix.add(str(a.val))

    if prefix:
        s = '\x1b[%sm%s%s'%( ";".join(prefix), s, postfix )
    return s
