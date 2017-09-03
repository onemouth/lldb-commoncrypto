import sys
sys.path.append("/Applications/Xcode.app/Contents/SharedFrameworks/LLDB.framework/Versions/Current/Resources/Python/")
import lldb

def handle_ptrace(frame, bp_loc, dict):
    pass

def anti_pt_deny_attach(debugger, command, result, internal_dict):
    """hi"""
    debugger.HandleCommand("b ptrace")
    debugger.HandleCommand("breakpoint command add 1")
    #debugger.HandleCommand("re w rdi 0")
    #debugger.HandleCommand("c")
    #debugger.HandleCommand("c")
    #debugger.HandleCommand("DONE")

def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand('command script add -f main.anti_pt_deny_attach anti_pt_deny_attach')
    print 'The "anti_pt_deny_attach" python command has been installed and is ready for use.'







