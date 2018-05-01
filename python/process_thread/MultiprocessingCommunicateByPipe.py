from multiprocessing import Process, Pipe
import os, time, random


# 多进程通信Pipe
def write(p):
    for value in ['A', 'B', 'C']:
        print('Put %s to queue...' % value)
        p.send(value)
        time.sleep(random.random())


def read(p):
    while True:
        value = p.recv()
        print('Get %s from queue.' % value)


if __name__ == '__main__':
    parent , child = Pipe()
    pw = Process(target=write, args=(parent,))
    pr = Process(target=read, args=(child,))
    pw.start()
    pr.start()
    pw.join()
    pr.terminate()
