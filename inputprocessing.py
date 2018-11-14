import sys
import os


def inputprocess(debug):
    # prompt
    sys.stdout.write("$ ")
    instr = sys.stdin.readline()
    # input cleansing
    instr = instr.replace("\n", '')
    instr = instr.replace("\t", ' ')
    instr = instr.lstrip(' ')
    splitin = instr.split(' ')
    # debug help
    if debug is True:
        sys.stdout.write("splitin is: ")
        print(splitin)
    # find and replace environment variables
    processed = []
    for i in splitin:
        if str.startswith(i, "$"):
            i = str.replace(i, "$", "")
            i = os.environ.get(i)
            if i is None:
                i = ""
            processed.append(i)
        else:
            processed.append(i)
    # debug help
    if debug is True:
        sys.stdout.write("processed is: ")
        print(processed)
    # find and replace e
    return processed
