# python day 20
# author zach.wang
# -*- coding:utf-8 -*-
import redis
#多任务操作
pool = redis.ConnectionPool(host='172.16.10.120', port=6379)

conn = redis.Redis(connection_pool=pool)

pipe = conn.pipeline()

pipe.set("ID","00001")
pipe.set("name","zach")
pipe.set("sex","UNKNOWN")

pipe.execute()

print(conn.get("ID").decode(),":",conn.get("name").decode(),":",conn.get("sex").decode())










