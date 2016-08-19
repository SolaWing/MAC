#!/usr/bin/env python
# encoding: utf-8

import os, plistlib, argparse, sys, re
#import PIL
from PIL import Image

def parse():
    parser = argparse.ArgumentParser(description = "export images from plist image")
    parser.add_argument("ifile", metavar = "input file", help ='input plist file')
    parser.add_argument("odir", metavar = "output dir", nargs = '?', 
        help = 'output dir to put out images, default the same name with input file')
    return parser.parse_args()

def evalStruct(evalStr):
    evalStr = evalStr.replace('{', '[').replace('}', ']')
    return eval(evalStr)

def main():
    args = parse()
    ifile = args.ifile #!!ifile =""
    odir = args.odir
    if odir is None: odir = ifile[:ifile.rindex('.')]
    #print ifile, odir
    index = plistlib.readPlist(ifile)
    plimg = index['metadata']['textureFileName']
    if plimg is None or plimg.rfind('.pvr') != -1: plimg = ifile[:ifile.rindex('.')] + '.png'
    else: plimg = os.path.join(os.path.dirname(ifile), plimg)
    if not os.path.exists(odir): os.mkdir(odir)
    elif not os.path.isdir(odir): print >> sys.stderr, "odir is a regular file!"; return
    # open image
    plimg = Image.open(plimg) #!! plimg = Image.new()
    for k,v in index["frames"].iteritems():
        isRotated = v['rotated']
        frame = evalStruct (v['frame'])
        offset = evalStruct (v['offset'])
        sourceSize = evalStruct( v['sourceSize'] )
        if isRotated: 
            subImg = plimg.crop((frame[0][0], frame[0][1], frame[0][0]+frame[1][1], frame[0][1]+frame[1][0]))
            subImg = subImg.transpose(Image.ROTATE_90)
        else: subImg = plimg.crop((frame[0][0], frame[0][1], frame[0][0]+frame[1][0], frame[0][1]+frame[1][1]))
        exportImg = Image.new('RGBA', sourceSize, color = (0,0,0,0))
        exportImg.paste(subImg, ((sourceSize[0]-frame[1][0])/2+offset[0], (sourceSize[1] - frame[1][1])/2 + offset[1]))
        exportImg.save(os.path.join(odir, k))


if __name__ == '__main__':
    main()
