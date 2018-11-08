import redis,sys
keys=sys.argv[1]
if len(sys.argv) < 2:
    print "At lease 2 arguments. Usage: python redis_del_keys.py [keys] [db_num]"
    exit(0)
if len(sys.argv) > 3:
    print "Too many arguments. Usage: python redis_del_keys.py [keys] [db_num]"
    exit(0)

if len(sys.argv)==3:
    db=sys.argv[2]
else:
    db=0

num = 0
pool = redis.ConnectionPool(host='redis-inside-prd-001.h28alp.0001.cnn1.cache.amazonaws.com.cn', port=7000, db=db)
r = redis.Redis(connection_pool=pool)

key_list = []
for key in r.scan_iter(match=keys, count=10000):
    key_list.append(key)
    num = num + 1
for key in key_list:
    r.delete(key)
print num,"keys deleted"
