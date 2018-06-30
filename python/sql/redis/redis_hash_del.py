# -*- coding: UTF-8 -*-
'''
    python redis_hash_del.py HASH_KEY_NAME
'''

# Import python libs
import sys
import redis

host = '192.168.0.118'
port = 6379
db = 0

# Args Input filter
if len(sys.argv) <= 1:
    print("python sys.argv[0] HASH_KEY_NAME")
    sys.exit()
else:
    hashkey = sys.argv[1]

# redis_hash_del online
def redis_hash_del(hashkey):
    '''
    delete redis hash key
    '''
    r = redis.Redis(host=host,port=port,db=0)
    if r.exists(hashkey):
        hashkey_all = r.hkeys(hashkey)
        for i in range(len(hashkey_all)):
	    r.hdel(hashkey, hashkey_all[i])
        print(i)
    else:
        print("KEY NOT EXISTS")

if __name__ == "__main__":
    redis_hash_del(hashkey)
