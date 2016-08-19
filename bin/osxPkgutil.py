#!/usr/bin/env python
# encoding: utf-8

import subprocess, os, sys, plistlib, argparse, re, time, shutil

def parse():
    parser = argparse.ArgumentParser(description = "help util of pkgutil, main propose is to show pkg and uninstall it!")
    parser.add_argument('-u', type=str, help="uninstall specified package")
    parser.add_argument('-s', type=str, help="t:time, l:location, n:name. output sorted info, current only support sort install time")
    parser.add_argument('-l', type=str, help="list specified package files")
    return parser.parse_args()

pat = re.compile(r'\s*([^:]+):\s*(\S*)')
def convertPkg(pkgname):
    if pkgname:
        proc = subprocess.Popen(['/usr/sbin/pkgutil', '--pkg-info', pkgname], stdout = subprocess.PIPE)
        infos = proc.stdout.read()
        pkginfo = {}
        for kv in infos.split('\n'):
            m = pat.match(kv)
            if m:
                pkginfo[m.group( 1 )] = m.group( 2 )
        t = pkginfo.get('install-time')
        if t:
            pkginfo['install-time'] = time.strftime("%y%m%d-%H:%M",time.localtime(float(t)))
        return pkginfo
    return None

def getFiles(pkgname):
    pkginfo = convertPkg(pkgname)
    prefix = os.path.join(pkginfo['volume'], pkginfo['location'])
    proc = subprocess.Popen(['/usr/sbin/pkgutil', '--files', pkgname], \
            stdout=subprocess.PIPE)
    files = proc.stdout.read().split('\n')
    files = [os.path.join(prefix, f) for f in files if f]
    return files

def main():
    p = parse()
    print (p)
    if p.s:
        proc = subprocess.Popen(['/usr/sbin/pkgutil', '--pkgs'], stdout = subprocess.PIPE)
        pkgs = proc.stdout.read()
        #print(proc.returncode)
        pkgs = pkgs.split('\n')
        #print (pkgs)

        pkginfos = [convertPkg(pkg) for pkg in pkgs if pkg]
        # sort
        if p.s == 't':
            pkginfos.sort(key=lambda x:x['install-time'])
        elif p.s == 'l':
            pkginfos.sort(key=lambda x:x['location'])
        else:
            pkginfos.sort(key=lambda x:x['package-id'])

        for i in pkginfos:
            print(i)
    elif p.l:
        for i in getFiles(p.l):
            print (i)
    elif p.u:
        files = getFiles(p.u)
        for i in files:
            print (i)
        confirm = raw_input("sure for remove?Y/n:")
        if confirm == "Y":
            for i in files:
                if os.path.isfile(i):
                    print("move '%s' to Trash"%(i))
                    to = os.path.expanduser("~/.Trash/")
                    to = os.path.join(to, os.path.basename(i))
                    while os.path.exists(to):
                      to+="1"
                    shutil.move(i, to)
            subprocess.call(["/usr/sbin/pkgutil", "--forget", p.u])
    else:
        subprocess.call([ '/usr/sbin/pkgutil', '--pkgs' ])

if __name__ == '__main__':
    main()
