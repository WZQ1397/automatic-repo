import redis
import time
r = redis.StrictRedis(host='192.168.1.1', port=6379, db=1)
while 1 :
    r.set('model_update_timestamp',int(time.time()*1000))
    # time.sleep(0.1)
    print('time update')
