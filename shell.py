from os import dup2
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


# small file cleanup
def clean(finfile, foutfile):
    if finfile is not None:
        finfile.close()
    if foutfile is not None:
        foutfile.close()


# program loop
while True:
    splitin, finfile, foutfile = inputprocess(debug)
    # builtin commands (including no command)
    try:
        bi[splitin[0][0]](splitin[0][1:])
        clean(finfile, foutfile)
        continue
    except KeyError:
        nop()
    # Process a real command
    pid = fork()
    if pid == 0:
        try:
            if finfile is not None:
                dup2(finfile.fileno(), 0)
            if foutfile is not None:
                dup2(foutfile.fileno(), 1)
            execvp(splitin[0][0], splitin[0])
        except OSError:
            print("Command not found.")
            exit()
    else:
        clean(finfile, foutfile)
        waitpid(pid, 0)

# TODO: pipes
# TODO: PS2 Prompt
# TODO: Tab features
# TODO: Colors
# TODO: Quote support
