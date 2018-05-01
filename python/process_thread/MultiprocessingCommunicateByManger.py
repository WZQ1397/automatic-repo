from multiprocessing import Process,Manager
import random

# PTA 重排链表
def exchange(L1, L2, L3):
    L2.reverse()
    x ,y = L1, L2
    z = []
    while L1 and L2:
        L3.append(L2[0])
        L3.append(L1[0])
        L1.pop(0)
        L2.pop(0)

    while L1:
        L3.append(L1[0])
        L1.pop(0)
    while L2:
        L3.append(L2[0])
        L2.pop(0)


if __name__ == '__main__':
    with Manager() as manager:
        num1 = input("list1:")
        num2 = input("list2:")
        sortedlist = manager.list()
        p = Process(target=exchange, args=(list(num1), list(num2), sortedlist))
        p.start()
        p.join()
        print("".join(sortedlist))
        p.terminate()
