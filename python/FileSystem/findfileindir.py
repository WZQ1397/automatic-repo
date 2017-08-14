#python day 6
#author zach.wang
import os, time, sys
from datetime import datetime
dir = "E:\\python"
savedir = "E:\python\zach.log"

def rescuresearch(lst,suffix,tmplist):
    flag = len(suffix)
    if os.path.isdir(lst):
        for sublst in os.listdir(lst):
            rescuresearch(sublst,suffix,tmplist)
    else:
        if flag>1:
            if os.path.splitext(lst)[1] == suffix:
                print(lst)
                tmplist.append(lst)
        else:
            print(lst)

def searchall(suffix=""):
    #global file
    file = input("do you want save result to file:[y/N]:\n")
    tmplist = []
    for lst in os.listdir(dir):
        print(lst.center(50, '-'))
        root = os.path.join(dir,lst)
        mtime = datetime.fromtimestamp(os.path.getmtime(root)).strftime('%Y-%m-%d %H:%M')
        print(mtime.center(30,"#").center(50," "))
        rescuresearch(root,suffix,tmplist)
    savetofile(file,tmplist,suffix)
'''
DIR="E:\\python"
for root, dirs, files in os.walk(DIR):
    print(files)
'''
def savetofile(file,tmplist,suffix):
    if file.lower() == "y":
        with open(savedir,"w") as fp:
            for lst in tmplist:
                fp.write(lst+"\n")
                sys.stdout.write("#")
                sys.stdout.flush()
                time.sleep(0.03)
            fp.write("Total Nums of File".center(30,"*").center(50," ")+"\n")
            fp.write("%10s %5d"%(suffix,tmplist.__len__()))
        print("\n\nfile save to",savedir,"success!")
        time.sleep(1)
    else:
        print("Total Nums of File".center(30,"*").center(50," "))
        print("%10s %5d"%(suffix,tmplist.__len__()))

def searchtype():
    suffix = input("please input what suffix you want:\n")
    if len(suffix) < 1:
        print("ERROR SYNTAX!")
        exit(1)
    searchall(suffix)

if __name__ == '__main__':
    print("\033[31;1m please Type dir or suffix for\033[0m","what do you want to find?\n")
    choose = input("All file under this dir or specify suffix of file:\n")
    print(choose)
    if choose.lower() == "dir":
        searchall()
    elif choose.lower() == "suffix":
    # 指定扩展名
        searchtype()
    else:
        print("ERROR SYNTAX!")
        exit(1)

