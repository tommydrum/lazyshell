import sys
import os
import prompt
import askpy

def inputprocess(debug):
    # prompt
    ps0 = os.environ.get("PS0")
    if ps0 is None:
        ps0 = "$"
    sys.stdout.write(ps0 + " ")
    instr = sys.stdin.readline()
    # input cleansing
    instr = instr.replace("\n", '')
    instr = instr.replace("\t", ' ')
    instr = instr.lstrip(' ')

    # Splitting string into basic lists, with quote support
    splitin = [""] # instr.split(' ')
    count = 0
    quoteflag = False
    for letter in instr:
        if quoteflag is True:
            if letter == '\"':
                quoteflag = False
                splitin.append("")
                count += 1
            else:
                splitin[count] += letter
        else:
            if letter == '\"':
                quoteflag = True
            elif letter == ' ':
                splitin.append("")
                count += 1
            else:
                splitin[count] += letter
    # debug help
    if debug is True:
        sys.stdout.write("splitin is: ")
        print(splitin)
    # find and replace environment variables, and gather file input and output if requested
    processed = [[]]
    cur = 0
    fin = ""
    finflag = False
    fout = ""
    foutflag = False
    for i in splitin:
        if i == "":
            continue
        if finflag is False and foutflag is False:
            if str.startswith(i, "$"):
                i = str.replace(i, "$", "")
                i = os.environ.get(i)
                if i is None: # case that the env variable isn't set
                    i = ""
                processed[cur].append(i)
            elif i == '<':
                finflag = True
            elif i == '>':
                foutflag = True
            elif i == '|':
                processed.append([])
                cur += 1
            else:
                processed[cur].append(i)
        elif finflag is True:
            fin = i
            finflag = False
        elif foutflag is True:
            fout = i
            foutflag = False
    # debug help
    if debug is True:
        sys.stdout.write("processed is: ")
        print(processed)
        sys.stdout.write("processed __len__: ")
        print(processed.__len__())
        sys.stdout.write("fin is: ")
        print(fin)
        sys.stdout.write("fout is: ")
        print(fout)
    # deal with filein and out
    finfile = None
    foutfile = None
    try:
        if fin != "":
            finfile = open(fin, "r")
        if fout != "":
            foutfile = open(fout, "w")
    except IOError:
        print("Failed to open file for input/output direction")
        return "", None, None  # to abort command
    return processed, finfile, foutfile
