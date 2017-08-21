# python day 22
# author zach.wang
# -*- coding:utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, TEXT, and_, or_ ,func
from sqlalchemy.orm import sessionmaker
import pydays.RandomUserAndPassword,re

#====================模版===================↓
#下面要修改
username = "zach"
passwd = "123456"
host = "172.16.6.214"
dbname = "pytest"

engine = create_engine("mysql+pymysql://"+username+":"+passwd+"@"+host+"/"+dbname
                       ,encoding='utf-8', echo=False)
Base = declarative_base() #生成orm基类
num = 20

#创建表结构
def initTab():
    Base.metadata.create_all(engine)

def dropTab():
    Base.metadata.drop_all(engine)

#====================模版===================↑

class User(Base):
    __tablename__ = 'user2' #表名
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    password = Column(String(64))
    memo = Column(TEXT(500))

    def __repr__(self):
        return "(%s: %s --> %s)" %(self.id, self.name, self.password)

Session = sessionmaker(bind=engine)() #生成session实例
'''
for i in range(num):
    user_obj = User(name=randomname.get_userName(8),
                    password="123456",
                    memo="this is zach test") #生成你要创建的数据对象
    Session.add(user_obj) #把要创建的数据对象添加到这个session里， 一会统一创建

print(user_obj.name,user_obj.id) #此时也依然还没创建
Session.commit() #现此才统一提交，创建数据
'''
#my_user = Session.query(User).filter_by(username="zach").first()
my_user = Session.query(User).all()
res = str(re.compile(r'-->').split(str(my_user))[0])
print("\n",re.compile(r':').split(res)[-1])

print("\n",my_user[-5])

#print("\n",re.compile(r'\(').split(after_delvalue)[-1])
Session.query(User).filter(User.id == \
                           re.compile(r'\(').\
                           split(re.compile(r':').\
                                 split(str(Session.query(User).\
                                        filter(User.id > 2).first()))[0])[-1]).delete()
Session.rollback()
Session.commit()
print("\n",Session.query(User).filter(User.id > 2).first())
print("\n",Session.query(User).filter(User.id > 2).filter(User.password=="123456").count())
print("\n",Session.query(User).filter(User.id .between(5,10)).filter(User.password=="123456")[1:5])
print("\n",Session.query(User).filter(or_(User.id.in_([5,6,7,15,18]),User.password=='123456'))[-3:-1])
print("\n",Session.query(User).filter(and_(User.name.ilike("y%"),User.id.notin_([5,6,7]))).all())
print("\n",Session.query(User).filter(or_(~User.name.ilike("y%"),
                                          ~User.name.ilike("%7%"))).order_by(User.name.desc(),User.id.asc()).all())
print("\n",Session.query(func.sum(User.id),User.name).group_by(User.name)[0:3])
#comperhensive
print("\n",Session.query(User.name).
      filter(User.id.in_(Session.query(User.id).
             filter(and_(or_(User.name.ilike("%w%"),User.name.ilike("%z%"),User.name.ilike("%q%")),
                         and_(~User.name.ilike("%x%"),~User.name.ilike("%y%"),~User.name.ilike("%c%")))).
             order_by(User.id.desc()).first())).all())








