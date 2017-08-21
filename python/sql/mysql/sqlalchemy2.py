# python day 24
# author zach.wang
# -*- coding:utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, TEXT, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, relationships
from pydays import RandomUserAndPassword
import random

#====================模版===================↓
#下面要修改
username = "zach"
passwd = "123456"
host = "172.16.6.214"
dbname = "pytest"

engine = create_engine("mysql+pymysql://"+username+":"+passwd+"@"+host+"/"+dbname
                       ,encoding='utf-8', echo=True)
Base = declarative_base() #生成orm基类
Session = sessionmaker(bind=engine)() #生成session实例

class User(Base):
    __tablename__ = 'user' #表名
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32),nullable=False)

    def __repr__(self):
        return "(%s: [%s.%s])" %(self.id, __name__, self.name)

class Group(Base):
    __tablename__ = 'group' #表名
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32),nullable=False)

    def __repr__(self):
        return "(%s: [%s.%s])" %(self.id, __name__, self.name)

class Group_User(Base):
    __tablename__ = 'GU_rela' #表名
    guid = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32),nullable=False)
    uid = Column(Integer,ForeignKey('user.id'))
    gid = Column(Integer,ForeignKey('group.id'))

    def __repr__(self):
        return "(%s: [%s.%s])" %(self.id, __name__, self.name)

#TODO IMPORTANT!
#Base.metadata.create_all(engine)

obj = Session.query(Group.name,User.name).all()
print(obj)