#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess, os, argparse

def parse():
    parser = argparse.ArgumentParser(description='xcodebuild help script')
    parser.add_argument('-c', '--configuration', default='Release',
                        help = 'configurations, default Release')
    parser.add_argument('-s', '--schema', action='append',
                        help='schema use to build, can specify multiple times')
    parser.add_argument('-d', '--destination', action='append',
                        default = ['platform=iOS Simulator,name=iPhone 5', 'generic/platform=iOS'],
                        help='build destination, can specify multiple times, default to iOS platform and simulator')
    parser.add_argument('-w', '--workspace', help = 'workspace use to build')
    parser.add_argument('-u', '--universal', action='store_false', help='flag to build universal libraries')

    return parser.parse_args()

def main():
    pass

if __name__ == "__main__":
    main()
