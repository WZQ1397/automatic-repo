import sys, re, os
 
def getDictList(dict):
    regx = '''[\w\~`\!\@\#\$\%\^\&\*\(\)\_\-\+\=\[\]\{\}\:\;\,\.\/\<\>\?]+'''
    with open(dict) as f:
        data = f.read()
        return re.findall(regx, data)
 
def rmdp(dictList):
    return list(set(dictList))
 
def fileSave(dictRmdp, out):
    with open(out, 'a') as f:
        for line in dictRmdp:
            f.write(line + '\n')
 
def main():
    try:
        dict = sys.argv[1].strip()
        out = sys.argv[2].strip()
    except Exception, e:
        print 'error:', e
        me = os.path.basename(__file__)
        print 'usage: %s <input> <output>' %me
        print 'example: %s dict.txt dict_rmdp.txt' %me
        exit()
 
    dictList = getDictList(dict)
    dictRmdp = rmdp(dictList)
    fileSave(dictRmdp, out)
     
if __name__ == '__main__':
    main()
