#!/usr/bin/env python
# coding=utf-8

import os, sys, shutil, threading, time, argparse
from collections import deque as deque

copyList = deque()
encList = deque()
luaList = deque()
threadCount = 1
alive = True
modifiedFileCount = 0

compileLua = False
encryptWithAES = False
aesKey = "b0ed50d4b43878ba9384443d783b5d997b2438e66e8eda4b40651aa5c747831b"
aesSuffix = "*"
aesSign = "CLSXHY"
luajit='lua'

def copy(src, dst):
    '''copy file or dir to a dir  or  copy file to a filePath'''
    if os.path.exists(src):

        if os.path.isdir(src):
            if not os.path.exists(dst):
                os.makedirs(dst)
            elif not os.path.isdir(dst):
                print ("error! copy directory to a exist file %s!"%(dst))
                return

            base = os.path.dirname(src)
            # walk src and filter file or dir start with .
            for r,dirs,files in os.walk(src):
                relpath = os.path.relpath(r, base)
                dstR = os.path.join(dst, relpath)
                if not os.path.exists(dstR):
                    os.makedirs(dstR)
                for f in files: 
                    if f.startswith("."): continue #ignore file begin with .

                    s,d = os.path.join(r,f) , os.path.join(dstR,f)
                    putTaskIntoList(s,d)

                dirs[:] = [d for d in dirs if not d.startswith(".")]
        else:
            needMakeDirs = []
            directory = dst
            # reversed check if path is contain a dir
            while True:
                directory = os.path.dirname(directory)
                if directory:
                    if os.path.exists(directory):
                        if os.path.isdir(directory):
                            break
                        else:
                            print ("error, path exists as a file")
                            return
                    else:
                        needMakeDirs.append(directory)
                else: break

            for directory in reversed( needMakeDirs ):
                if not os.path.exists(directory):
                    os.mkdir(directory)

            if os.path.isdir(dst):
                # copy same name file into the dir
                d = os.path.join(dst, os.path.basename(src))
                putTaskIntoList(src,d)
            else:
                putTaskIntoList(src, dst)

def putTaskIntoList(s, d):
    # 修改时间小于一定值认定未变动. 如果是同一文件, 时间肯定一样的,就自动过滤了
    # print "addTask %s >>>> %s"%(s,d),
    if ( not os.path.exists(d) or abs(os.path.getmtime(s) - os.path.getmtime(d)) > 5 ):
        #print " done"

        # 是否编译lua文件
        if compileLua and s.endswith(".lua"):
            luaList.append( (s, d) )
        # 是否加密
        elif encryptWithAES and ( ("*" in aesSuffix) or (s[(s.rfind('.')) : ] in aesSuffix)):
            encList.append( (s, d) )
        # 否则只复制
        else:
            copyList.append( (s, d) )
        global modifiedFileCount
        modifiedFileCount += 1
    
def copyThread():
    while alive:
        if len(copyList) > 0:
            src, dst = copyList.popleft()
            print ("copyFile", dst)
            shutil.copy2(src, dst)
        elif len(encList) > 0:
            src, dst = encList.popleft()
            print ("encFile", dst)
            s = "openssl enc -aes-256-ecb -in '%s' -out '%s' -K '%s'"%(src, dst, aesKey)
            os.system(s)
            with open(dst,"ab") as f:
                f.write(aesSign)
            shutil.copystat(src, dst) # 最后要复制文件附加属性用来做是否改变的判定
        elif len(luaList) > 0:
            src, dst = luaList.popleft()
            print ("compile luaFile", dst)
            s = "%s -O3 -b -g '%s' '%s'"%(luajit, src, dst)
            os.system(s)
            shutil.copystat(src, dst)
        else:
            time.sleep(1)

def hasTask():
    """子线程是否有任务"""
    return len(copyList) > 0 or len(encList) > 0 or len(luaList) > 0

def startThread():
    global alive
    alive = True
    for x in range(threadCount):
        t = threading.Thread(target = copyThread)
        t.start()

def stopThread():
    global alive
    alive = False

def getParser():
    import argparse
    parser = argparse.ArgumentParser(description = "copy inconsistent file or dir to a dir\nthat is, only copy the file which is modified, status 0 show no change, 1 show has change")
    parser.add_argument('source', type = str, nargs = '+', help = "source file or source directory, may be multiple")
    parser.add_argument('destination', type=str, help = "destination file or destination dir")
    parser.add_argument('-e','--encrypt', action="store_true", help = "if encrypt file with aes")
    parser.add_argument('-s','--suffix', type=str, default="*", help = "the suffix of file which need to be encrypted")
    parser.add_argument('-c','--compileLua', action="store_true", help="if compile lua file")

    return parser

def main():
    parser = getParser()
    args = parser.parse_args()

    global aesSuffix, compileLua, encryptWithAES
    aesSuffix = args.suffix
    compileLua = args.compileLua
    encryptWithAES = args.encrypt

    # multi thread

    startThread()

    st = time.time()

    for f in args.source:
        src = os.path.abspath(f)
        dst = os.path.abspath(args.destination) 
        print (src , dst)
        copy(f, args.destination)

    while hasTask():
        time.sleep(1)

    stopThread()

    print("used time", time.time() - st)

    if modifiedFileCount > 0: sys.exit(1)

if __name__ == '__main__':
    main()
