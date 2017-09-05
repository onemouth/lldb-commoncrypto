from __future__ import print_function
import os
import sys
import time
sys.path.append("/Applications/Xcode.app/Contents/SharedFrameworks/LLDB.framework/Versions/Current/Resources/Python/")
import lldb

debugger = lldb.SBDebugger.Create()
debugger.SetAsync(False)

def anti_pt_deny_attach(breakpoint, frame, bpno):
    global debugger
    print("Hit ptrace breakpoint")
    debugger.HandleCommand("re w rdi 0")

def main():
    exe = sys.argv[1]
    #debugger = lldb.SBDebugger.Create()
    #debugger.SetAsync(False)
    global debugger
    print("Creating a target for '%s'" % exe)
    target = debugger.CreateTargetWithFileAndArch(exe, lldb.LLDB_ARCH_DEFAULT)
    if not target:
        print("Failed to Create the target")
        sys.exit(1)
    
    ptrace_bp = target.BreakpointCreateByName("ptrace")
    print(ptrace_bp)
    ptrace_bp.SetScriptCallbackFunction("anti_pt_deny_attach")
    process = target.LaunchSimple(None, None, os.getcwd())
    if not process:
       print("Failed to Launch the process") 
       sys.exit(2)
    print(process)
    while True:
        if process.GetState() == lldb.eStateStopped:
            debugger.HandleCommand("c")
        elif process.GetState() == lldb.eStateExited:
           print("process exited")
           sys.exit(1)
        else:
            print("Unknown status")
            print(process.GetState())
        time.sleep(1)
         
if __name__ == "__main__":
    main()





