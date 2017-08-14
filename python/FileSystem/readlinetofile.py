#python day 3
#author zach.wang

openstack = open('iplist.bin', 'r+')
zach = open('filter.txt', 'a+')
def readXlinetofile(count=20):
    i = 0
    start = zach.tell()
    while i < count:
        zach.write(openstack.readline())
        i += 1
    print("make success!") if start < zach.tell() and zach.readable() else print("ERROR!")

readXlinetofile(10)
