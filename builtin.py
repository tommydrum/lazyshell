import os


# Module functions


# directory nav
def curdir(args):
    print(os.getcwd())


def chdir(args):
    try:
        os.chdir(args[0])
    except OSError:
        print("Failed")


def listdir(args):
    for i in os.listdir(os.getcwd()):
        if os.path.isfile(i):
            print("File\t" + i)
        elif os.path.isdir(i):
            print("Dir\t" + i)
        else:
            print("Other\t" + i)


# other shell features
def setenv(args):
    try:
        envvar = args[0]
        setvar = args[1]
    except IndexError:
        print("Not enough arguments")
        print("syntax: set key value")
        return
    os.environ[envvar] = setvar


# helpers
def fakeexit(args):
    exit()


nop = lambda *a, **k: None


# init builtin functions, NEEDS TO STAY AT END
def initbuiltin():
    functions = {
        "exit": fakeexit,
        "e": fakeexit,  # alias for myself..
        "dir": curdir,
        "cwd": curdir,
        "ls": listdir,
        "cd": chdir,
        "chdir": chdir,
        "set": setenv,
        '': nop
    }
    return functions
