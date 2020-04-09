#!/usr/bin/env python3
# encoding: utf-8

import sys,os

if __name__ == '__main__':
    sys.path.insert(0, r'/Applications/Xcode.app/Contents/SharedFrameworks/LLDB.framework/Versions/A/Resources/Python')

import lldb, re
from lldb import SBDebugger, SBThread, SBProcess, SBTarget, SBFrame

def getSelectedFrame(obj):
    if isinstance(obj, SBDebugger):
        return obj.GetSelectedTarget().GetProcess().GetSelectedThread().GetSelectedFrame()
    elif isinstance(obj, SBThread):
        return obj.GetSelectedFrame()
    elif isinstance(obj, SBProcess):
        return obj.GetSelectedThread().GetSelectedFrame()
    elif isinstance(obj, SBTarget):
        return obj.GetProcess().GetSelectedThread().GetSelectedFrame()
    return None
def getSelectedThread(obj):
    if isinstance(obj, SBDebugger):
        return obj.GetSelectedTarget().GetProcess().GetSelectedThread()
    elif isinstance(obj, SBTarget):
        return obj.GetProcess().GetSelectedThread()
    elif isinstance(obj, SBProcess):
        return obj.GetSelectedThread()
    return None

def disassemble(debugger, command, result, internal_dict):
    """
    abbreviation of disassemble
    if match '^$', will be disassemble -p
    else match '\s*(f)?([+-]\d+)?\s*(\d+)?\s*(.*)'
            fromBegin, startOffset, num, other_argu = r.groups()
    :type debugger: lldb.SBDebugger
    :type command: str
    :type result: lldb.SBCommandReturnObject
    :type internal_dict: dict
    """
    if re.match("^$", command):
        debugger.HandleCommand('disassemble -p')
    else:
        # f: if disassemble from begin
        # +-offset : if disassemble from back(-) offset lines or front(+) offset lines
        # num : the disassemble lines number
        # other_argu : will pass to disassemble
        r = re.match("\s*(f)?([+-]\d+)?\s*(\d+)?\s*(.*)", command)
        if r :
            fromBegin, startOffset, num, other_argu = r.groups()
            #print >> result, fromBegin, startOffset, num
            start = ""
            hasP = ""
            if startOffset:
                # this var may not work
                frame = debugger.GetSelectedTarget().GetProcess().GetSelectedThread().GetSelectedFrame()
                #!! frame=lldb.SBFrame
                dis = frame.disassembly
                #  print >> result, dis
                if dis:
                    pc = "0x%x"%frame.pc
                    #  print >> result, pc
                    addr = re.findall("(0x[0-9a-fA-F]+)\s*(?:<[^>]*>)?\s*:", dis)
                    lenAddr = len(addr)
                    #  print >> result, addr
                    if lenAddr > 0:
                        index = 0
                        try:
                            index = addr.index(pc)
                            index += int(startOffset, 0)
                            if index < 0: index = 0
                            if index >= lenAddr : index = 0
                        except Exception as e:
                            pass
                        start = "-s %s"%addr[index]

            elif fromBegin: hasP = ''
            else: hasP = "-p"

            if num: num = "-c %s"%num
            else: num = ""
            com = 'disassemble %s %s %s %s'%(hasP, start, num, other_argu)
            #  print >> result , com
            debugger.HandleCommand(com)
        else :
            debugger.HandleCommand('disassemble %s'%command)

def findModule(debugger, command, result, internal_dict):
    """
    find modules alias
    empty will call target modules list
    else match '\s*(\S+)\s*(\d+)?\s*(.*)'
            keyword, moduleIndex, other_argu = r.groups()
    finally exe 
            command = 'target modules lookup -Ar -n %s %s "%s"'%(keyword, other_argu, modulePath)
    :type debugger: lldb.SBDebugger
    :type command: str
    :type result: lldb.SBCommandReturnObject
    :type internal_dict: dict
    """
    print(command)
    if re.match('^$', command):
        debugger.HandleCommand('target modules list')
    else:
        # keyword : the name to search . regex syntax
        # num : the module index 
        # other_argu : will pass to 'target modules lookup'
        r = re.match(r'\s*(\S+)\s*(\d+)?\s*(.*)', command)
        print(r.groups())
        if r:
            keyword, moduleIndex, other_argu = r.groups()
            modulePath = ''
            if moduleIndex:
                moduleIndex = int(moduleIndex)
            else:
                moduleIndex = 0

            #lldb.SBTarget.GetModuleAtIndex
            if moduleIndex >=0 : 
                m = debugger.GetSelectedTarget().GetModuleAtIndex(moduleIndex) #!! m=lldb.SBModule
                if m:
                    modulePath = m.GetPlatformFileSpec().fullpath #!!modulePath = ""
            command = 'target modules lookup -Ar -n %s %s "%s"'%(keyword, other_argu, modulePath)
            print(command)
            debugger.HandleCommand(command)
        else:
            debugger.HandleCommand('target modules list')

def regVariable(debugger, command, result, internal_dict):
    """
    abbreviation of frame variable -r
    :type debugger: lldb.SBDebugger
    :type command: str
    :type result: lldb.SBCommandReturnObject
    :type internal_dict: dict
    """
    if re.match('^$', command):
        debugger.HandleCommand("frame variable")
    else:
        #frame = debugger.GetSelectedTarget().GetProcess().GetSelectedThread().GetSelectedFrame()
        #!! frame=lldb.SBFrame
        
        debugger.HandleCommand("frame variable -r %s"%(command))

def continueTo(debugger, command, result, internal_dict):
    """
    short for thread until -f <currentFrame> -- $linenum. or passthrough to thread until
    :type debugger: lldb.SBDebugger
    :type command: str
    :type result: lldb.SBCommandReturnObject
    :type internal_dict: dict
    """
    r = re.match(r'\s*(?:(0x[0-9a-fA-F]+)|(\d+))', command)
    if r:
        frame = getSelectedFrame(debugger) # type: SBFrame
        fid = frame.GetFrameID()
        if r.group(1):
            s = "thread until -f %d -a %s"%(fid, r.group(1))
        else:
            s = "thread until -f %d -- %s"%(fid, r.group(2))
        print(s)
        debugger.HandleCommand(s)
    else:
        debugger.HandleCommand("thread until %s"%(command))

def printToFile(debugger, command, result, internal_dict):
    """
    print to a tmp file, default "/tmp/lldb.out"
    :type debugger: lldb.SBDebugger
    :type command: str
    :type result: lldb.SBCommandReturnObject
    :type internal_dict: dict
    """
    if not command: return
    outputFile = internal_dict.get("customOutputFile")
    if not outputFile:
        outputFile = open("/tmp/lldb.out", "wb")
        internal_dict["customOutputFile"] = outputFile

    origin_file = debugger.GetOutputFileHandle()
    debugger.SetOutputFileHandle(outputFile, False)
    debugger.HandleCommand(command)
    debugger.SetOutputFileHandle(origin_file, False)

def step_func(debugger, command, result, internal_dict):
    thread = debugger.GetSelectedTarget().GetProcess().GetSelectedThread()

    start_num_frames = thread.GetNumFrames()
    if start_num_frames == 0:
        return

    while True:
        thread.StepInstruction(0)
        if thread.GetNumFrames() != start_num_frames:
            stream = lldb.SBStream()
            thread.GetStatus(stream)
            description = stream.GetData()

            print("Call stack depth changed %d -> %d" % (start_num_frames, thread.GetNumFrames()), file=result)
            print(description, file=result)

            break

def __lldb_init_module(debugger, internal_dict):
    """
    :type debugger: lldb.SBDebugger
    :type internal_dict: dict
    """
    pymap = {
        "d":  "customCommand.disassemble",
        "fm": "customCommand.findModule",
        "fr": "customCommand.regVariable",
        "to": "customCommand.continueTo",
        ">":  "customCommand.printToFile",
        "sf": "customCommand.step_func",
    }
    for k, v in pymap.items():
        s = 'command script add -f %s %s'%(v,k)
        debugger.HandleCommand(s)

if __name__ == '__main__':
    lldb.debugger = lldb.SBDebugger.Create()

