# python day 24
# author zach.wang
# -*- coding:utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, TEXT, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, relationships
from pydays import RandomUserAndPassword
import random, time, platform, subprocess

# ====================模版===================↓
# 下面要修改
username = "zach"
passwd = "123456"
host = "172.16.6.214"
dbname = "pytest"

engine = create_engine("mysql+pymysql://" + username + ":" + passwd + "@" + host + "/" + dbname, encoding='utf-8',
                       echo=True)
Base = declarative_base()  # 生成orm基类
num = 20
Ctbl = "Human"
Mtbl = "Gun"


# 创建表结构
def initTab ():
    Base.metadata.create_all(engine)


def dropTab ():
    Base.metadata.drop_all(engine)
    Session.commit()


def initdata ():
    for i in range(num):
        Creator_obj = Creator(name=RandomUserAndPassword.get_userName(8), password="123456", memo="this is zach test")
        Session.add(Creator_obj)

    Gunlist = ['AK47', 'M4A1', "A58", 'PP75', 'MP7', 'MR220', 'C99']
    for j in range(len(Gunlist)):
        Machine_obj = Machine(name=Gunlist[j], rank=random.randrange(1, 5), memo="this is zach test")
        Session.add(Machine_obj)

    Session.commit()

    selectlst = []
    for k in range(1, num):
        k2 = 0
        while k2 < random.randrange(1, 3):
            Dist_Mid = random.randint(1, len(Gunlist))
            selectlst.append(Dist_Mid)
            k2 += 1
        '''
                if k2 == 0:
                selectlst.append(Dist_Mid)
                k2 += 1
            else:
                for check in selectlst:
                    if check == Dist_Mid:
                        continue
        '''
        Creator_Machine_obj = Creator_Machine(Cid=k, Mid=Dist_Mid, memo=str(k) + " --> " + str(Gunlist[Dist_Mid - 1]))
        Session.add(Creator_Machine_obj)
        Session.commit()


# ====================模版===================↑

class Creator(Base):
    __tablename__ = Ctbl  # 表名
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32), nullable=False)
    password = Column(String(64), nullable=False)
    memo = Column(TEXT(500))

    def __repr__ (self):
        return "(%s: [%s.%s] --> %s)" % (self.id, __name__, self.name, self.password)


class Machine(Base):
    __tablename__ = Mtbl  # 表名
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32), nullable=False)
    rank = Column(Float(precision=3))
    memo = Column(TEXT(500))

    def __repr__ (self):
        return "(%s: [%s] --> %s)" % (self.id, self.name, self.rank)


class Creator_Machine(Base):
    __tablename__ = str(Ctbl) + str(Mtbl)  # 表名
    CMid = Column(Integer, primary_key=True, autoincrement=True)
    Cid = Column(Integer, ForeignKey('{}.id'.format(Ctbl)))
    Mid = Column(Integer, ForeignKey('{}.id'.format(Mtbl)))
    memo = Column(TEXT(500))

    def __repr__ (self):
        return "%s:(%s --> %s)[%s]\n" % (self.CMid, self.Cid, self.Mid, self.memo)


def zachinit (lock, target):
    initTab()
    initdata()
    with open(target, "w") as f:
        f.write("1")


class InitDB(object):
    def __init__ (self, flag=0):
        lock = 'zach.lock'
        sysinfo = str(platform.system())
        self.flag = flag
        if sysinfo == "Windows":
            target = 'D:\\' + lock
            if subprocess.getoutput('more ' + target) == '1':
                # and subprocess.getoutput('cat '+lock) == '1':
                x = str(input("do you want reestabish table struct?"))
                if x.lower() == "yes" or x.lower() == "y":
                    dropTab()
                    time.sleep(1)
                    zachinit(lock, target)
                    self.flag = 1
                else:
                    self.flag = 2
                    exit(0)
            else:
                zachinit(lock, target)
                self.flag = 1
        elif sysinfo.capitalize() == "Linux":
            target = '/var/' + lock
            if subprocess.getoutput('cat ' + target) == '1':
                x = str(input("do you want reestabish table struct?"))
                if x.lower() == "yes" or x.lower() == "y":
                    dropTab()
                    time.sleep(1)
                    zachinit(lock, target)
                    self.flag = 1
                else:
                    self.flag = 2
                    exit(0)
            else:
                zachinit(lock, target)
                self.flag = 1

    def __repr__ (self):
        if self.flag == 1:
            return "Init success!"
        elif self.flag == 2:
            return "Init Abort!"
        else:
            return "Init Failed!"


Session = sessionmaker(bind=engine)()  # 生成session实例
InitDB()
time.sleep(1)

print(Session.query(Creator_Machine).all())
