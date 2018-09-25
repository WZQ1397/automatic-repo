class Node(object):

    def __init__(self, init_data):
        self.data = init_data
        self.next = None


class NewList(object):

    def __init__(self):
        self.head = None

    def is_empty(self):
        if self.head is None:
            print('链表为空')

# 在链表前添加节点
    def add(self, item):
        temp = Node(item)
        if self.head is None:
            self.head = temp
        else:
            temp.next = self.head
            self.head = temp
            print(id(self.head),id(temp),id(self.head.data),id(temp.data))

    def append(self, item):
        temp = Node(item)
        origin = self.head
        if self.head is None:
            self.head = temp
        else:
            while origin.next is not None:
                origin = origin.next
            else:
                origin.next = temp

    def search(self, item):
        origin = self.head
        flag = False
        while origin is not None:
            if origin.data == item:
                print('你要找的元素在里面')
                flag = True
                break
            else:
                origin = origin.next
        if flag is False:
            print('未找到')

    def location(self, item):
        location = 0
        origin = self.head
        lista = []
        while origin is not None:
            if origin.data == item:
                lista.append(location)
            origin = origin.next
            location += 1
        print(lista)

    def index(self, item):
        origin = self.head
        count = 0
        while origin is not None:
            if origin.data == item:
                count += 1
                break
            else:
                origin = origin.next
        if count != 0:
            print(count-1)
        else:
            print('未找到')

# 删除所有值为item的节点
    def delete(self, item):
        if self.head is None:
            print('链表是空的')
        else:
            while True:
                if self.head.data == item:
                    self.head = self.head.next
                else:
                    break
            previous = self.head
            current = previous.next
            while current is not None:
                if current.data == item:
                    previous.next = current.next
                    current = current.next
                    continue
                else:
                    previous = current
                    current = current.next

# 仿照列表中的remove方法
    def remove(self, item):
        flag = False
        if self.head is None:
            print('链表是空的')
        else:
            if self.head.data == item:
                self.head = self.head.next
            else:
                previous = self.head
                current = self.head.next
                while flag is False:
                    if current.data == item:
                        previous.next = current.next
                        flag = True
                    else:
                        previous = current
                        current = current.next
        if flag is True:
            print('已经移除')
        else:
            print('未找到相应的数字')

# 遍历单链表中的值
    def bianli(self):
        current = self.head
        lista = []
        while current is not None:
            lista.append(current.data)
            current = current.next
        print(lista)

# 删除链表制定位置上的节点
    def delnode(self, index):
        # current 代表当前位置
        # previous 代表上一个位置
        # 一开始都指向head
        current = self.head
        previous = self.head
        if index == 1:
            self.head = self.head.next
        else:
            # 用来定位指定位置,执行一次current往后挪一个，previous也后移一个
            for i in range(index-1):
                if current.next is None:
                    print('超出了范围')
                    break
                else:
                    print('成功执行')
                    previous = current
                    current = current.next
                    # 此时current到了指定的位置上
            # 未超出范围,执行删除操作
            else:
                previous.next = current.next

# 查看链表的长度：
    def len(self):
        length = 0
        current = self.head
        while current is not None:
            length += 1
            current = current.next
        return length

# 有了len（）之后,删除制定节点的另一种方法
    def deleNode(self, index):
        if self.head is None:
            print('链表为空')
        elif index > self.len():
            print('超出范围')
            return
        elif index == 1:
            self.head = self.head.next
        else:
            previous = self.head
            current = previous.next
            count = 2
            # 因为删除的那个节点一定存在所以while true没问题
            while True:
                if index == count:
                    previous.next = current.next
                    break
                else:
                    previous = current
                    current = current.next
                    count += 1

# 指定位置前插入节点
    def insert(self, index, value):
        if self.head is None:
            print('链表为空')
        if index > self.len():
            print('链表超出范围')
        elif index == 1:
            self.add(value)
        elif index == self.len()+1:
            self.append(value)
        else:
            count = 2
            previous = self.head
            current = self.head.next
            while True:
                if count == index:
                    temp = Node(value)
                    temp.next = current
                    previous.next = temp
                    break
                else:
                    previous = current
                    current = current.next
                    count += 1

# 删除链表以及内部的所有元素
    def clear(self):
        self.head = None

# 获得指定位置节点的值
    def getvalue(self, index):
        if self.head is None :
            return '链表为空'
        elif index > self.len():
            return '链表超出长度'
        else:
            count = 1
            current = self.head
            while True:
                if index != count:
                    current = current.next
                    count += 1
                else:
                    return current.data

# 仿pop：获取链表尾部的值，并删除该尾部的节点
    def pop(self):
        if self.head is None:
            return '当前链表为空'
        elif self.head.next is None:
            temp = self.head.data
            self.head = None
            return temp
        else:
            current = self.head
            while current.next.next is not None:
                current = current.next
            temp2 = current.data
            current.next = None
            return temp2

# 逆向链表
    def reverse(self):
        if self.head is None or self.head.next is None:
            return '链表就一个，或者没有 逆向没意义'
        else:
            previous = None
            current = self.head
            while current is not None:
                # post 关键了！如果我直接修改current.next，没有了指向下一节点的引用，链表直接断咯～
                post = current.next
                current.next = previous
                previous = current
                current = post
            # 把最后一个节点的头给揪出来，不然无从下手啊～
            self.head = previous

# 去重
    def delrepeat(self):
        if self.head is None or self.len() == 1:
            return
        else:
            # 用一个字典来储存data出现的次数
            dic = {}
            temp = self.head
            # 先遍历一波，给所有的data 作为键 值都为0，作为初始化
            while temp is not None:
                dic[str(temp.data)] = 0
                temp = temp.next
            previous = None
            current = self.head
            while current is not None:
                # 如果值出现过了，那么它的值就是1，删除
                if dic[str(current.data)] == 1:
                    previous.next = current.next
                    # 这个很关键，删掉了之后，我的current还要继续向后延伸，因为我还要继续检查后面的
                    current = current.next
                else:
                    # 第一次出现，打上标签记为1
                    dic[str(current.data)] += 1
                    previous = current
                    current = current.next

    # 删除链表中最小的元素
        def del_minimal(self):
            current = self.head
            min = self.head.data
            while current is not None:
                if current.data < min:
                    min = current.data
                current = current.next
            self.delete(min)

---------------------

本文来自 NoobIn江湖 的CSDN 博客 ，全文地址请点击：https://blog.csdn.net/qq_41376740/article/details/79171165?utm_source=copy 
