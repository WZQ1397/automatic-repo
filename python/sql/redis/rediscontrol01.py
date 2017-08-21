# python day 20
# author zach.wang
# -*- coding:utf-8 -*-
import redis,time

conn = redis.Redis(host='172.16.10.120', port=6379)
conn.set("zach","51xyc")
conn.lpush("lst1","1","2","3")
conn.hmset("zach_hac",{"1":"yes","0":"no","255":"error"})
print(conn.get("zach").decode())
print(conn.llen("lst1"))
print(conn.lrange("lst1",0,-1))
#其他部分
print(conn.exists("zach"))
print(conn.type("lst1"),conn.delete("lst1"))
print(conn.exists("lst1"),conn.keys("*"),conn.hmget("zach_hac",{"1","0"}))
conn.expire("zach_hac",5)
time.sleep(6)
print("\n ============ \nfin_result:\n",conn.exists("zach_hac"),conn.keys("*"))









