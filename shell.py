from os import dup2
from os import fork
from os import execvp
from os import waitpid
from os import pipe
from os import close
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
        close(finfile)
    if foutfile is not None:
        close(foutfile)


# Process command
def processcmd(cmd, finfile, foutfile):
    # builtin commands (including no command)
    try:
        bi[cmd[0]](cmd[1:])
        clean(finfile, foutfile)
        return None
    except KeyError:
        nop()
    # Process a real command
    pid = fork()
    if pid == 0:
        try:
            if finfile is not None:
                dup2(finfile, 0)
            if foutfile is not None:
                dup2(foutfile, 1)
            execvp(cmd[0], cmd)
        except OSError:
            print("Command not found.")
            exit()
    else:
        clean(finfile, foutfile)
        return pid


# program loop
while True:
    cmdlist, finfile, foutfile = inputprocess(debug)
    finfileno = None
    foutfileno = None
    if finfile is not None:
        finfileno = finfile.fileno()
    if foutfile is not None:
        foutfileno = foutfile.fileno()
    cmdcount = cmdlist.__len__() - 1
    pidlist = []
    r1, w1 = pipe()
    r2, w2 = pipe()
    i = 0
    for l in cmdlist:
        # reusing two pipes over, alternating between read and write ends.
        tmp = i % 2
        if i % 2 == 0:
            readend = r2
            writeend = w1
        else:
            readend = r1
            writeend = w2
        if cmdcount == 0: # only in chain
            pidlist.append(processcmd(l, finfileno, foutfileno))
        elif i == 0 and i != cmdcount: # first in chain
            pidlist.append(processcmd(l, finfileno, w1))
        elif i != 0 and i != cmdcount: # middle of chain
            pidlist.append(processcmd(l, readend, writeend))
        elif i == cmdcount: # end of chain
            pidlist.append(processcmd(l, readend, foutfileno))
        # recreate used pipes
        if i % 2 == 0:
            r2, w2 = pipe()
        else:
            r1, w1 = pipe()
        i += 1
    for l in pidlist:
        if l is not None: # essentially skips builtin commands..
            waitpid(l, 0) # wait for all processes in chain at once.
# TODO: PS2 Prompt
# TODO: Tab features
# TODO: Colors
# TODO: Quote support
