import re
import os
import sys
from time import sleep
from colorama import init as colorama_init
from colorama import Fore, Back, Style

colorama_init()


def writeFile(fname, buffer):
    f = open(fname, "w")
    text = f.write(buffer)
    f.close()

def pass1(fname):
    pattern = re.compile("static .*.\\\\u[A-F0-9]{4}.*\)\n.*\n.*return .*\;")
    f = open(fname, "r")
    text = f.read()
    f.close()

    m = pattern.findall(str(text))
    lines = text.split("\n")
    newbuffer = ""

    replace_table = ['to_find', 'to_replace']
    rellist = []

    for itms in m:

        x = re.search("(\\\\u.*\\\\u[A-F0-9]{4}).*\)\n.*\n.*return (.*)\;", itms)
        # print(x.group())
        tofind = x.group(1)
        replace_with = x.group(1)
        if x.group(2).find(".") >= 0:
            replace_with = "_".join(x.group(2).split("."))
            replace_with = replace_with.split("(")[0]
        elif x.group(2).find(" ") >= 0:
            replace_with = "_".join(x.group(2).split(" "))
            replace_with = replace_with.split("(")[0]
        rellist.append(dict(zip(replace_table, [tofind, replace_with])))

    for line in lines:
        # print(Style.BRIGHT + Fore.WHITE + Back.GREEN + line + Style.RESET_ALL)
        # print(Style.BRIGHT + Fore.WHITE + Back.BLUE + x.group(1) + Style.RESET_ALL)
        # rint(Style.BRIGHT + Fore.WHITE + Back.YELLOW + "_".join(x.group(2).split(".")) + Style.RESET_ALL)
        for rep_list in rellist:
            if line.find(rep_list['to_find']) >= 0:
                line = line.replace(rep_list['to_find'], rep_list['to_replace'])
                break
        '''
        try:
            for i in range(5):
                sleep(0.3)
        except KeyboardInterrupt:
            pass
        '''
        newbuffer += line
        newbuffer += "\n"

    return  newbuffer

def fill_list(list_one, idx):
    list_two = []
    for itms in list_one:
        list_two.append(itms[idx])
    return list_two

def pass_(buffer, renamer_list):
    newbuffer = ""

    lines = buffer.split("\n")

    for line in lines:
        for rep_list in renamer_list:
            if line.find(rep_list['to_find']) >= 0:
                line = line.replace(rep_list['to_find'], rep_list['to_replace'])
                break
        newbuffer += line
        newbuffer += "\n"

    return newbuffer


def pass2(buffer):

    renamer = ['to_find', 'to_replace']
    renamer_list = []
    mlist = []
    flist = []
    clist = []


    pattern_methods = re.compile("((\\\\u[A-Fa-f0-9]{4}){10,1000})[\(\<]")
    pattern_fields = re.compile("((\\\\u[A-Fa-f0-9]{4}){10,1000})[ ;\n,]")
    pattern_classes = re.compile("((\\\\u[A-Fa-f0-9]{4}){10,1000})[\.]")
    pattern_extra = re.compile("((u[A-F0-9]{4}_){5,600}u[A-F0-9]{4})")

    f = pattern_fields.findall(buffer)
    m = pattern_methods.findall(buffer)
    c = pattern_classes.findall(buffer)
    e = pattern_extra.findall(buffer)

    mlist = fill_list(m,0)
    flist = fill_list(f,0)
    clist = fill_list(c,0)
    elist = fill_list(e,0)

    for idx, itms in enumerate(mlist):
        replace_with = "Method_" + str(idx)
        renamer_list.append(dict(zip(renamer, [itms, replace_with])))

    buffer = pass_(buffer, renamer_list)

    for idx, itms in enumerate(flist):
        replace_with = "field_" + str(idx)
        renamer_list.append(dict(zip(renamer, [itms, replace_with])))

    buffer = pass_(buffer, renamer_list)

    for idx, itms in enumerate(clist):
        replace_with = "Class_" + str(idx)
        renamer_list.append(dict(zip(renamer, [itms, replace_with])))

    buffer = pass_(buffer, renamer_list)

    for idx, itms in enumerate(elist):
        replace_with = "Name_" + str(idx)
        renamer_list.append(dict(zip(renamer, [itms, replace_with])))

    buffer = pass_(buffer, renamer_list)

    return buffer

def pass3(buffer):
    newbuffer = ""
    pattern = re.compile(".*num[0-9]? = .*\n")
    m = pattern.findall(buffer)
    replist = []
    for matches in m:
        tmo = matches
        tmo = tmo.replace("num","005500")
        if re.search("[A-Za-z]{3,1000}", tmo) == None:
            replist.append(matches)
    lines = buffer.split("\n")
    for line in lines:
        for itms in replist:
            try:
                ln = line.strip("\t")
                ln = ln.strip("\n")
                itms = itms.strip("\t")
                itms = itms.strip("\n")
                #print(ln,itms)
                if ln.find(itms) >= 0:
                    line = ""
            except Exception as e:
                print(itms, str(e))
                sleep(10)
        newbuffer += line
        newbuffer += "\n"
    return newbuffer

def main():
    fname = sys.argv[1]

    fname_cleaned = os.path.splitext(fname)
    fname_cleaned = ".".join([fname_cleaned[0] + "_cleaned", fname_cleaned[1]])

    buffer = pass1(fname)
    for i in range(3):
        buffer = pass2(buffer)
    buffer = pass3(buffer)

    writeFile(fname_cleaned, buffer)


if __name__ == "__main__":
    main()