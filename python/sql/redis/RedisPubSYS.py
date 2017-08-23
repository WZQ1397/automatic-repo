# python day 21
# author zach.wang
# -*- coding:utf-8 -*-
import redis

# redis_pub =
class RedisPubSYS(object):

    def __init__ (self,redis_hostname,redis_port):
        # pool = redis.ConnectionPool(host=, port=)
        self.__conn = redis.Redis(host=redis_hostname, port=redis_port)

    def redis_publish (self, __pub = "zach", msg=""):
        pub = self.__conn
        pub.publish(__pub, msg)
        return True

    def redis_subscribe (self, __sub = "zach"):
        sub = self.__conn.pubsub()
        sub.subscribe(__sub)
        sub.parse_response()
        return sub
