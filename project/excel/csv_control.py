import json
import os,re
import csv,pprint
path = 'E:\\ssd\\psync'
csvpath = 'E:\\zach.csv'

class CSV(object):
    def __init__(self,path,csvpath):
         self.path = path
         self.csvpath=csvpath

    def zach_csvwrite(self,csvfmt):
        #TODO CSV写操作
        out = open(self.csvpath,'a',newline = "")
        zach_csv = csv.writer(out,dialect='excel')
        zach_csv.writerow(csvfmt)
        out.close()
        return True

    def zach_csvread(self,rtype='normal'):
        with open(self.csvpath, "r", encoding = "utf-8") as f:
            if rtype == 'normal':
                reader = csv.reader(f)
            else:
                reader = csv.DictReader(f)
            rows = [row for row in reader]
        return rows

EXEC_CSV = CSV(path,csvpath)

#TODO 详细内容插入
def zach(files):
    for f in files:
        filename = f.split('.')[0]
        filepath = '{path}\{f}'
        realpath = filepath.format(path = path,f = f)
        with open(realpath) as f:
            data = json.load(f)
            if 'randr' in realpath:
                level = data['jobs'][0]['read']
                s = (level['iops'])
                t = (level['clat']['mean'])
            if 'randw' in realpath:
                level = data['jobs'][0]['write']
                s = (level['iops'])
                t = (level['clat']['mean'])
            #print (filename+","+str(s))
        #TODO CSV写操作
        EXEC_CSV.zach_csvwrite([filename,str(s),str(t)])

def insert():
    files = os.listdir(path)
    EXEC_CSV.zach_csvwrite(['Type',"iops","lantcy"])
    zach(files)

def show():
    pprint.pprint(EXEC_CSV.zach_csvread())

insert()
show()