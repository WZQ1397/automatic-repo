import os,random

for f in os.listdir('E:\\blog\\article'):
    linkherf = "article/" + f
    month = str(random.randint(1,3))
    day = str(random.randint(1,28))
    day = "0"+day if len(day) <2 else day
    print( "<li><span>18-{0}-{1})</span><a href=\"#\" class=\"link1\">[CEPH]</a> <a href={2}>{3}</a></li>"
          .format(month,day,linkherf,os.path.basename(f)))
