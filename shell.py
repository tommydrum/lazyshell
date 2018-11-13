import os
import sys

if sys.argv.__contains__("-v"):
    debug = True
    print("Verbosity is enabled.")
else:
    debug = False
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

    # builtin commands (including no command)
    if splitin[0] == "exit":
        exit()
    if splitin[0] == '':
        continue

    # Process a real command
    id = os.fork()
    if id == 0:
        os.execvp(splitin[0], splitin)
    else:
        os.waitpid(id, 0)

#TODO: replace $var with environment variables
#TODO: file redirection
#TODO: pipes