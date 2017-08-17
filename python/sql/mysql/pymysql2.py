# python day 21
# author zach.wang
# -*- coding:utf-8 -*-
import pymysql

conn = pymysql.connect(host='172.16.6.214',port=3306,user='zach',passwd='123456',db='pytest')
num = 20
startnum = 1000
point = conn.cursor()
point.execute("select count(*) from zach2")
curnum = point.fetchone()[0]
print(curnum)

try:
    with conn.cursor() as point:
        i, name = startnum, "wzq"
        sql = "insert into zach2(id,name) values(%s,%s)"
        while i < startnum + num:
            i += 1
            point.execute(sql, (i,name+str(i)))
        else:
            print("{} SQL has insert success!".format(num))
    conn.commit()

    with conn.cursor() as point:
        sql = "select * from zach2"
        point.execute(sql)
        point.scroll(curnum,mode="absolute")
        print("After insert first item:\n{}\n".format(point.fetchone()))
        point.scroll(num - 2)
        print("After insert last item:\n{}\n".format(point.fetchone()))

finally:
    conn.close()