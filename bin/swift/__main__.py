#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os
import asyncio
from .compiler import Compiler

#################### MAIN
def main():
    import logging
    logging.basicConfig()

    import argparse
    parser = argparse.ArgumentParser(description="generate swift entity graph")
    parser.add_argument("-l", "--xcodelog", default="-", help="xcode compile log file, default use stdin")
    parser.add_argument("-c", "--cache_directory", help="cache dir, default will output to temp dir" )
    parser.add_argument("--overwrite", action="store_true", help="overwrite file in output_directory")
    parser.add_argument("modules", nargs="*", default=None, help="module named need index")
    args = parser.parse_args()

    if args.xcodelog == "-":
        xcodelog = sys.stdin.read()
    else:
        with open(args.xcodelog) as f:
            xcodelog = f.read()

    compiler = Compiler.from_xcode_log(xcodelog, cache_dir = args.cache_directory, overwrite = args.overwrite)
    asyncio.get_event_loop().run_until_complete(
        compiler.index(args.modules)
    )

if __name__ == "__main__":
    main()
