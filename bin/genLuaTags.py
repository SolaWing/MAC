#!/usr/bin/env python
# encoding: utf-8

import os, sys, re, argparse

def parse():
    parser = argparse.ArgumentParser(description = "generate tags of lua file and bottom c,cpp files")
    parser.add_argument('-o', '--output', default=".tags", type=str, help="the output files")
    parser.add_argument('files', nargs='*', default=['.'], help="the file path or folder use to gen tags")
    ret = parser.parse_args()
    return ret

def main():

    args = parse()

    ctags = "xtags"
    tagFile = args.output

    lang="--languages='C,C++,Lua'"
    fields = "--fields=+l"
    files = ' '.join(args.files)
    cmd = "%s -R -f %s %s %s -u %s"%(ctags, tagFile, lang, fields, files)
    print ( cmd )
    os.system(cmd)
    print("change Language!")
    changeLangToLua(tagFile)
    print ("trancateLua!")
    trancateLua(tagFile)

def changeLangToLua(inputFileName, outputFileName=None):
    """
    change language flag to lua so lua file can use c,c++ tag in YCM
    """
    if not outputFileName: outputFileName = inputFileName

    with open(inputFileName) as f:
        s = f.read()

    s = re.sub(r'(?<=\slanguage:)[^lL]\S*', 'Lua', s)
    with open(outputFileName, "w") as f:
        f.write(s)
    

def trancateLua(inputFileName, outputFileName=None):
    """
    remove the class of lua tag, so tag can search the method directly
    remove the empty space before the \t
    """
    if not outputFileName: outputFileName = inputFileName

    with open(inputFileName) as f:
        s = f.read()

    s = re.sub(r"^\w+[\.:](?=.+?\.lua)", "", s, flags = re.MULTILINE)
    # normal group will cause some match replace to ^A, I don't know why , but use name group is fine
    s = re.sub(r"^(?P<p>[^\t]*?) +\t", "\g<p>\t", s, flags = re.MULTILINE)
    # delete invalid tag , which has invalid char before \t
    s = re.sub(r"^\S* .*$\n", "", s, flags = re.MULTILINE)

    ss = s.split('\n')
    ss = sorted(set(ss), lambda x,y: cmp(x,y))
    print "len,", len(ss)
    with open(outputFileName, "w") as f:
        for s in ss:
            if s:
                f.write(s + "\n")

if __name__ == '__main__':
    main()


