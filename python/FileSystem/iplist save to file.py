#python day 2
#author zach.wang
import sys
#create ip list by truple and list
scope_list = (6, 7, 8, 10, 33, 56)
serv_list = []
with open('iplist.bin', 'w+') as file:
    sys.stdout = file
    for scope in range(2, 252):
        serv_list.append(scope)
    for sub in range(90,115,4):
        serv_list.remove(sub)
    for scope in scope_list:
        for lst in serv_list:
            print('192.168.%d.%d'%(scope,lst))
    print("Total IP :",serv_list.__len__()*scope_list.__len__())

