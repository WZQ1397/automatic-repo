import time
import threading

# Semaphore(信号量)来实现

def get_thread_a(semaphore,i):
	time.sleep(1)
	print("get thread : {}".format(i))
	semaphore.release()


def get_thread_b(semaphore):
	for i in range(10):
		semaphore.acquire()
		thread_a = threading.Thread(target=get_thread_a, args=(semaphore,i))
		thread_a.start()


if __name__ == "__main__":
  # 调用一次semaphore.acquire()时，Semaphore的数量就减1，直至Semaphore数量为0时被锁上
	# 当release()后Semaphore数量加1。Semaphore在本质上是调用的Condition
	semaphore = threading.Semaphore(2)
	thread_b = threading.Thread(target=get_thread_b, args=(semaphore,))
	thread_b.start()