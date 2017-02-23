#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv, argparse
from lxml import etree as ET

def parse():
    parser = argparse.ArgumentParser(description="convert bug free xml to csv")
    parser.add_argument("xmlPath", help="bugfree export xml files")
    parser.add_argument("outPath", default=None, nargs='?', help="output path, default add extension csv")
    return parser.parse_args()

def parseXML(path):
    tree = ET.parse(path);
    ws = tree.find('{*}Worksheet')
    rows = map(
        lambda row: list(map(
            lambda x: "\t".join(x.text.splitlines()) if x.text else ""
            ,row.iterfind('{*}Cell/{*}Data')))
        ,ws.iterfind('.//{*}Row')
    )
    return rows

def main():
    env = parse()
    rows = list(parseXML(env.xmlPath))
    outPath = env.outPath if env.outPath else env.xmlPath + ".csv"
    #  print(outPath)
    #  print(rows)
    with open(outPath, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)

if __name__ == "__main__":
    main()
