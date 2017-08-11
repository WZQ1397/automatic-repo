import re,os

PATH = 'E:\\TEMP\\salt\\squid3\\default\\squid.conf'
DUMP_PATH = PATH+'.dump'

def stripcommentline(reg):
    with open(PATH) as f:
        if os.path.exists(DUMP_PATH):
            os.remove(DUMP_PATH)
        for str in f:
            with open(DUMP_PATH,'a') as w:
                if reg.search(str).__class__ ==  reg.search("").__class__ :
                    w.write(str)
        with open(DUMP_PATH,'r') as f:
            for str in f:
                print(str,end='') if re.search(r'[^\s]',str) else print(end='')

stripcommentline(re.compile(r'#'))