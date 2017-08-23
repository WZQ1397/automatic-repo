# python day 21
# author zach.wang
# -*- coding:utf-8 -*-
import sys

from RedisPubSYS import RedisPubSYS

target = RedisPubSYS("172.16.10.120","6379")
try:
    if len(sys.argv) <= 2:
        target.redis_publish(sys.argv[1])
    if len(sys.argv) > 2:
        target.redis_publish(sys.argv[1],sys.argv[2])
        print(sys.argv[1],sys.argv[2])
except (AttributeError,IndexError) as e:
    print(e,"failed to publish")


