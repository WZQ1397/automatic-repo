import threading
import time

# 线程不同步

def get_thread_a():
    print("get thread A started")
    time.sleep(3)
    print("get thread A end")


def get_thread_b():
    print("get thread B started")
    time.sleep(5)
    print("get thread B end")


if  __name__ == "__main__":
    thread_a = threading.Thread(target=get_thread_a)
    thread_b = threading.Thread(target=get_thread_b)
    start_time = time.time()
		# 子线程在主线程运行结束后，会继续执行完
		# 如果给子线程设置为守护线程(setDaemon=True)，主线程运行结束子线程即结束
    thread_b.setDaemon(True)
    thread_a.start()
    thread_b.start()
		# 如果join()线程，那么主线程会等待子线程执行完再执行。
    thread_a.join()

    end_time = time.time()
    print("execution time: {}".format(end_time - start_time))