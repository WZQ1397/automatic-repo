# python day 21
# author zach.wang
# -*- coding:utf-8 -*-
import redis

class OnlineCheckState(object):
    def __init__(self,host,port,keyname,password=""):
        if password == "":
            self.conn = redis.Redis(host=host, port=port)
        else:
            self.conn = redis.Redis(host=host, port=port, password=password)
        self.keyname = keyname

    def onlinecheck(self,pid,Missionstate):
        if Missionstate == 0:
            self.conn.setbit(self.keyname,pid,value=1)
        else:
            self.conn.setbit(self.keyname,pid,value=0)

    #统计还有多少将在执行
    def onlinecount(self):
        return self.conn.bitcount()

    def __repr__(self):
        print(self.conn)

#OnlineCheckState(host='172.16.10.120', port=6379).onlinecount()



