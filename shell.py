from os import fork
from os import execvp
from os import waitpid
from sys import argv
from builtin import initbuiltin
from builtin import nop
from inputprocessing import inputprocess

# init
bi = initbuiltin()

# debug flag
if argv.__contains__("-v"):
    debug = True
    print("Verbosity is enabled.")
else:
    debug = False

# program loop
while True:
    splitin = inputprocess(debug)
    # builtin commands (including no command)
    try:
        bi[splitin[0]](splitin[1:])
        continue
    except KeyError:
        nop()
    # Process a real command
    pid = fork()
    if pid == 0:
        try:
            execvp(splitin[0], splitin)
        except OSError:
            print("Command not found.")
            exit()
    else:
        waitpid(pid, 0)

# TODO: file redirection
# TODO: pipes
