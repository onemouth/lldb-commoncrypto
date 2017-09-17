from __future__ import print_function
import os
import sys
import base64
import time
import csv
sys.path.append("/Applications/Xcode.app/Contents/SharedFrameworks/LLDB.framework/Versions/Current/Resources/Python/")
import lldb

debugger = lldb.SBDebugger.Create()
debugger.SetAsync(False)
global process

def anti_pt_deny_attach(frame, bplo, data):
    global debugger
    print("Hit ptrace breakpoint")
    debugger.HandleCommand("re w rdi 0")

def handle_esi(regs, data_dict):
    for reg in regs:
        if reg.GetName() == "esi":
            alg = reg.GetValueAsUnsigned()
            print("alg: {}".format(alg))
            data_dict["alg"] = alg

def handle_r8(regs, data_dict):
    for reg in regs:
        if reg.GetName() == "r8":
            # guess this is `keylen` param
            data_dict["keylen"] = reg.GetValueAsUnsigned()

def handle_rcx(regs, data_dict):
    for reg in regs:
        if reg.GetName() == "rcx":
            # guess this is `key` param
            print('Name: ', reg.GetName(), ' Value: ', reg.GetValue())
            error = lldb.SBError()
            content = process.ReadMemory(reg.GetValueAsUnsigned(), data_dict['keylen'], error)
            if error.Success():
                data_dict["key"] = base64.b64encode(content)

def create_read_register(frame, bplo, data):
    global debugger
    global process
    print("Hit read register breakpoint")
    #print(type(frame))
    regs_set = frame.GetRegisters()
    for regs in regs_set:
         if 'general purpose registers' in regs.GetName().lower():
            data_dict = {}
            handle_esi(regs, data_dict)
            handle_r8(regs, data_dict)
            handle_rcx(regs, data_dict)
            if "alg" in data_dict:
                writer.writerow(data_dict)

def main():
    global writer
    global debugger
    global process
    exe = sys.argv[1]
    cccreate_csv_file = sys.argv[2]
    cccreate_csv = open(cccreate_csv_file, "w")
    fieldnames = ['alg', 'keylen', "key"]
    writer = csv.DictWriter(cccreate_csv, fieldnames=fieldnames)
    writer.writeheader()

    #debugger = lldb.SBDebugger.Create()
    #debugger.SetAsync(False)
    print("Creating a target for '%s'" % exe)
    target = debugger.CreateTargetWithFileAndArch(exe, lldb.LLDB_ARCH_DEFAULT)
    if not target:
        print("Failed to Create the target")
        sys.exit(1)
    
    ptrace_bp = target.BreakpointCreateByName("ptrace")
    cccrypto_create_bp = target.BreakpointCreateByName("CCCryptorCreate")
    print(ptrace_bp)
    ptrace_bp.SetScriptCallbackFunction("anti_pt_deny_attach")
    cccrypto_create_bp.SetScriptCallbackFunction("create_read_register")
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
           cccreate_csv.close()
           sys.exit(1)
        else:
            print("Unknown status")
            print(process.GetState())
        time.sleep(1)
         
if __name__ == "__main__":
    main()





