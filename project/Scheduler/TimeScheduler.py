import time,sched
#任务永久循环调用
scheduler = sched.scheduler(time.time, time.sleep)

def print_event(name, start):
    now = time.time()
    elapsed = int(now - start)
    print('EVENT: {} elapsed={} name={}'.format(
        time.ctime(now), elapsed, name))
    if elapsed > 20:
        exit(0)
    fun()

def fun():
    scheduler.enter(10, 2, print_event, ('10', start))
    scheduler.enter(20, 1, print_event, ('20', start))

start = time.time()
print('START:', time.ctime(start))
fun()
scheduler.run()