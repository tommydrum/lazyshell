import os
import sys
import io

# Module functions

# no-op
nop = lambda *a, **k: None

#directory nav
def curdir(args):
    print(os.getcwd())

def chdir(args):
    try:
        os.chdir(args[0])
    except OSError:
        print("Failed")

def listdir(args):
    for i in os.listdir(os.getcwd()):
        print(i)
        #todo: differentiate directories from files

# init builtin functions
def initbuiltin():
    functions = {
        "exit": exit,
        "dir": curdir,
        "cwd": curdir,
        "ls": listdir,
        "cd": chdir,
        '': nop
    }
    return functions

# init
bi = initbuiltin()


# debug flag
if sys.argv.__contains__("-v"):
    debug = True
    print("Verbosity is enabled.")
else:
    debug = False

# program loop
while True:
    # prompt
    sys.stdout.write("$ ")
    instr = sys.stdin.readline()

    # input cleansing
    instr = instr.replace("\n", '')
    instr = instr.replace("\t", '')
    instr = instr.lstrip(' ')
    splitin = instr.split(' ')
    if debug is True:
        sys.stdout.write("splitin is: ")
        print(splitin)
        sys.stdout.write("args is: ")
        print(splitin[1:])

    # builtin commands (including no command)
    try:
        bi[splitin[0]](splitin[1:])
        continue
    except KeyError:
        nop()

    # Process a real command
    id = os.fork()
    if id == 0:
        try:
            os.execvp(splitin[0], splitin)
        except OSError:
            print("Command not found.")
            exit()
    else:
        os.waitpid(id, 0)

#TODO: replace $var with environment variables
#TODO: file redirection
#TODO: pipes
