# python day 23
# author zach.wang
# -*- coding:utf-8 -*-
import sys
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, BOOLEAN
from sqlalchemy.orm import sessionmaker

def check_db (username, passwd, host, dbname):
    global engine, Base
    engine = create_engine("mysql+pymysql://" + username + ":" + passwd + "@" + host + "/" + dbname, encoding='utf-8',
                           echo=False)
    Base = declarative_base()  # 生成orm基类


class Check(Base):
    __tablename__ = 'check_state'  # 表名
    pid = Column(Integer, autoincrement=True, primary_key=True)
    pname = Column(String(32))
    state = Column(BOOLEAN)

    def __repr__ (self):
        return "(%s: %s --> %s)" % (self.pid, self.pname, self.state)


Session = sessionmaker(bind=engine)()  # 生成session实例


def check_state (value, misson_name):
    global judge
    if value == 0:
        print("Mission Success!")
        judge = 0
    else:
        sys.stderr.write("Error! Mission Failed")
        judge = 1
    check_obj = Check(pname=misson_name, state=judge)
    Session.add(check_obj)


def total_state ():
    ok = Session.query(Check).filter(Check.state == 0).count()
    err = Session.query(Check).filter(Check.state == 1).count()
    return ok, err
