#!/usr/bin/env python
# encoding: utf-8

import subprocess, cStringIO, os,sys

class ITermSource(object):

    """a osascript cmd"""

    def __init__(self):
        self.cmd = []

    def __lshift__(self, cmd):
        if (isinstance(cmd, basestring)): self.cmd.append(cmd)
        elif (isinstance(cmd, ITermSource)): self.cmd.extend(cmd.cmd)
        return self

    def execute(self):
        cmd = r"""
tell application "iTerm"
%s
end tell
"""%'\n'.join(self.cmd)

        (out,err) = subprocess.Popen(["osascript"], stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE) \
            .communicate(cmd)
        if out: print "out", out
        if err: print "err", err
        return out

def createSendTextCmd(text, session=None):
    osasource = r"""
	if not (exists current terminal) then
		set s to launch (make new terminal) session ""
	else
		set s to current session of current terminal
	end if
	write s text "%s"
"""

    # escape ["\]
    sio = cStringIO.StringIO()
    for c in text:
        if c in '"\\': sio.write("\\")
        sio.write(c)
    text = sio.getvalue()
    sio.close()

    return osasource%text

def sendText(s, isActivate=False):
    source = ITermSource()
    source << createSendTextCmd(s)
    if isActivate: source << "activate"
    source.execute()

def test():
    sendText('''
  print 222
  print 223
''', True)

def main():
    s = sys.stdin.read()
    sendText(s, True)

if __name__ == '__main__':
    main()
