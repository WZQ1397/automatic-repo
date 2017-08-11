# python day 18
# author zach.wang
# -*- coding:utf-8 -*-
import gevent,threading

count1 ,count2 = 0, 0
def diffSyncandAsync(num,sel):
    global count1,count2
    if sel.lower() == "sync":
        count1 += 1
        print("this is {}, {}th".format(sel,count1))
        gevent.sleep(1)
    elif sel.lower() == "async":
        count2 += 1
        print("this is {}, {}th".format(sel,count2),threading.current_thread())
        gevent.sleep(1)
    else:
        pass

def sync(value):
    hifen = "-"*20

    while count1 < value:
        diffSyncandAsync(value,"sync")
    print(hifen.center())
    
    thread = [ gevent.spawn(diffSyncandAsync,count2,"async") for count2 in range(value)]
    gevent.joinall(thread)

    print(hifen.center(40))
    threadlst = []
    for count2 in range(value):
        threadlst.append(count2)
    for T in threadlst:
        realthread = threading.Thread(target=diffSyncandAsync,args=[T,"async"])
        realthread.start()

sync(10)