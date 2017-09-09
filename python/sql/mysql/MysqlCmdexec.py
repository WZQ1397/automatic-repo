#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-

import pymysql
import sys

#重点
sql = "SELECT * FROM `kvt` LIMIT 0, 1000"

connection = pymysql.connect(host='localhost', user='dev', passwd='dEvp@ssw0rd', db='test', port=3306,
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)

try:
    with connection.cursor() as cursor:
        cursor.execute(sql)
    connection.commit()
finally:
    connection.close()
if cursor is not None:
    results = [result for result in cursor]
    print results
    for result in results:
        for key, value in result.items():
            print key, value
else:
    print('This will never be reached when join gevent')
    sys.exit(1)