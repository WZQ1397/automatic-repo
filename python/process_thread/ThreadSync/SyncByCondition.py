import threading

# condition(条件变量)，实现线程同步
# Condition内部有一把锁，默认是RLock可重入锁
# RLock可以在同一个线程里面连续调用多次acquire()，但必须再执行相同次数的release()
# 解决平台锁造成死锁的问题
def get_thread_a(condition):
	with condition:
		condition.wait()
		print("A : Hello B,that's ok")
		condition.notify()
		condition.wait()
		print("A : I'm fine,and you?")
		condition.notify()
		condition.wait()
		print("A : Nice to meet you")
		condition.notify()
		condition.wait()
		print("A : That's all for today")
		condition.notify()


def get_thread_b(condition):
	# wait() ：允许等待某个条件变量的通知，notify()可唤醒
	# notify()： 唤醒等待队列wait()
	with condition:
		print("B : Hi A, Let's start the conversation")
		condition.notify()
		condition.wait()
		print("B : How are you")
		condition.notify()
		condition.wait()
		print("B : I'm fine too")
		condition.notify()
		condition.wait()
		print("B : Nice to meet you,too")
		condition.notify()
		condition.wait()
		print("B : Oh,goodbye")


if __name__ == "__main__":
	condition = threading.Condition()
	# condition(条件变量)，线程在执行时，当满足了特定的条件后，才可以访问相关的数据
	thread_a = threading.Thread(target=get_thread_a, args=(condition,))
	thread_b = threading.Thread(target=get_thread_b, args=(condition,))
	thread_a.start()
	thread_b.start()
	
'''
B : Hi A, Let's start the conversation
A : Hello B,that's ok
B : How are you
A : I'm fine,and you?
B : I'm fine too
A : Nice to meet you
B : Nice to meet you,too
A : That's all for today
B : Oh,goodbye
'''