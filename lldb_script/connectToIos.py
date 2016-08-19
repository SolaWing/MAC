#!/usr/bin/env python
# encoding: utf-8

if __name__ == '__main__':
    sys.path.insert(0, r'/Applications/Xcode.app/Contents/SharedFrameworks/LLDB.framework/Versions/A/Resources/Python')

import lldb, re
from lldb import SBDebugger, SBThread, SBProcess, SBTarget, SBFrame

def connectToIos(debugger, command, result, internal_dict):
    """
    pass port to connect, should init `idevicedebugserverproxy` first
    :type debugger: lldb.SBDebugger
    :type command: str
    :type result: lldb.SBCommandReturnObject
    :type internal_dict: dict
    """
    localPath = "/Users/mac/Library/Developer/Xcode/DerivedData/IfengNews-ezewegrapjqjtjdjncnmdneoglem/Build/Products/Debug-iphoneos/IfengNews.app"
    remotePath = "/var/mobile/Applications/91D9358A-FF9E-4494-9A64-9EA5C543910F/IfengNews.app"
    triple = "armv7s-apple-ios"
    platform = 'remote-ios'
    add_dependent_modules = False
    error = lldb.SBError()

    target = debugger.CreateTarget(localPath, triple, platform, add_dependent_modules, error)
    #import: must set ios file path
    target.modules[0].SetPlatformFileSpec(lldb.SBFileSpec(remotePath))
    process = target.ConnectRemote(target.GetDebugger().GetListener(), "connect://localhost:%s"%command, None, error)
    if process.IsValid():
        target.Launch(lldb.SBLaunchInfo([]), error)
    else:
        print "has error:", error.description

connectToIos(lldb.debugger, "3333", lldb.SBCommandReturnObject(), None)
