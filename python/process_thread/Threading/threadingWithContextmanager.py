#/usr/bin/python3
# -*- coding: utf-8 -*-

import threading
import time
from contextlib import contextmanager

# 管理 thread-local（线程局部的）数据
thread_local = threading.local()
local.tname = 'transfer_currence'

# 为函数设置上下文管理
@contextmanager
def acquire(*locks):
    #sort locks by object identifier
    locks = sorted(locks, key=lambda x: id(x))
    
    #make sure lock order of previously acquired locks is not violated
    acquired = getattr(thread_local,'acquired',[])
    if acquired and (max(id(lock) for lock in acquired) >= id(locks[0])):
        raise RuntimeError('Lock Order Violation')
    
    # Acquire all the locks
    acquired.extend(locks)
    thread_local.acquired = acquired
    
    try:
        for lock in locks:
            lock.acquire()
				# 获取完锁后跳转回with上下文，完成后回来
        yield
    finally:
				# 完成后释放锁
        for lock in reversed(locks):
            lock.release()
				# 删除所有的锁
        del acquired[-len(locks):]

class Account(object):
    def __init__(self, name, balance, lock):
        self.name = name
        self.balance = balance
        self.lock = lock
        
    def withdraw(self, amount):
				# 出账
        self.balance -= amount
        
    def deposit(self, amount):
				# 进账
        self.balance += amount
        
def transfer(from_account, to_account, amount):
		'''
		from_account: Account ==> a
		to_account: Account ==> b
		'''
    print("%s transfer..." % amount)
		# 使用with上下文获取锁 
    with acquire(from_account.lock, to_account.lock):
        from_account.withdraw(amount)
        time.sleep(1)
        to_account.deposit(amount)
    print("%s transfer... %s:%s ,%s: %s" % (amount,from_account.name,from_account.balance,to_account.name, to_account.balance))
    print("transfer finish")
    
if __name__ == "__main__":
    a = Account('a',1000, threading.Lock())
    b = Account('b',1000, threading.Lock())
    thread_list = []
		'''
		from_account: Account ==> a
		to_account: Account ==> b
		a ==> b : a send 100 to b
		a: 900  b: 1100
		'''
    thread_list.append(threading.Thread(target = transfer, args=(a,b,100)))
		'''
		from_account: Account ==> b
		to_account: Account ==> a
		b ==> a : b send 500 to a
		a: 1400  b: 900
		'''
    thread_list.append(threading.Thread(target = transfer, args=(b,a,500)))
    for i in thread_list:
        i.start()
    for j in thread_list:
        j.join()