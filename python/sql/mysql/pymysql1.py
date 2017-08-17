# python day 21
# author zach.wang
# -*- coding:utf-8 -*-
import pymysql,pydays.RandomUserAndPassword

conn = pymysql.connect(host='172.16.6.214',port=3306,user='zach',passwd='123456',db='pytest')
point = conn.cursor()
'''
point.execute("create table zach(id int,name char(16))")
point.executemany("insert into zach(id,name) values(%s,%s)",[("0001","zach"),("0002","xyc")])
point.execute("create table zach2(id int,name char(16))")

for i in range(20):
    point.execute("insert into zach2(id,name) values(%s,%s)", (i, randomname.get_userName(8)))
'''
point.execute("select * from user2")
'''
row_1 = point.fetchone()
#获取前n行数据
n = 3

row_2 = point.fetchmany(n)
print("first row item:\n",row_1,"{} rows items\n\n".format(n),row_2)
point.scroll(3,mode='absolute')
print("ALL values from current location to end:\n\n",point.fetchall())
point.scroll(-3)
'''
print("from current location to 3 before:\n\n",point.fetchall())
# 提交，不然无法保存新建或者修改的数据

conn.commit()
point.close()
