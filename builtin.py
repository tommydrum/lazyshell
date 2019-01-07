#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
# Module functions


# directory nav
def curdir(args):
    print(os.getcwd())


def chdir(args):
    try:
        os.chdir(args[1])
    except OSError:
        print("Failed")
    except IndexError:
        os.chdir(os.environ["HOME"])


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
        envvar = args[1]
        setvar = args[2]
    except IndexError:
        print("Not enough arguments")
        print("syntax: set key value")
        return
    os.environ[envvar] = setvar

def unset(args):
    try:
        envvar = args[1]
    except IndexError:
        print("Not enough arguments")
        print("syntax: unset key")
        return
    try:
        os.environ.__delitem__(envvar)
    except KeyError:
        print("Key not found.")

# helpers
def fakeexit(args):
    exit()

def nop(args = None):
    pass

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
        "unset": unset,
        '': nop()
    }
    return functions
