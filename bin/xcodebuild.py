#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import absolute_import

import subprocess, os, sys

def show_help():
    print("usage: " + __file__ +  " project targetname (other xcodebuild args...)")
    subprocess.check_call(["xcodebuild", "-help"], stdout = sys.stdout)
    exit()

def main():
    if any( a in ("-h", "--help", "help", "-help") for a in sys.argv[1:] ):
        show_help()

    project = sys.argv[1]
    assert project.endswith(".xcodeproj")

    target = sys.argv[2]



if __name__ == "__main__":
    main()
