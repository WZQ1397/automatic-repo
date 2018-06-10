#批量创建文件夹
#Author zach.wang
import sys
import os
name = sys.argv[1]
num = int(sys.argv[2])
if sys.argv.__len__() < 2:
    print("invalid parameter!")
else:
    if sys.argv.__len__() > 3:
        pre = sys.argv[3]
        post = sys.argv[4]
    else:
        pre = ""
        post = ""
    mydir =input("which dir you choose:")
    if mydir == "":
        mydir = "."
    os.chdir(mydir)
    for i in range(1,num):
        mydir = pre + name + str(i) + post
        os.mkdir(mydir)
tree = os.popen("tree").read()
print(tree)
