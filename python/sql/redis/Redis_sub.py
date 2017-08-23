# python day 21
# author zach.wang
# -*- coding:utf-8 -*-
import RedisPubSYS
import sys


def redissub(channel):
    target = RedisPubSYS.RedisPubSYS("172.16.10.120", "6379")
    redis_sub = target.redis_subscribe(channel)
    while True:
        msg = redis_sub.parse_response()
        print("channel:\t"+channel ,":",msg[-1].decode())
if len(sys.argv) <2:
    redissub("zach")
else:
    redissub(sys.argv[1])

