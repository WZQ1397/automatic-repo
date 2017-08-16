# python day 19
# author zach.wang
# -*- coding:utf-8 -*-
import pika,sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange="zach_d",type="direct")
if len(sys.argv) > 2:
    print("only send to first level!")
msg = "{} message.{}" .format(sys.argv[1:2],sys.argv[-1:])
channel.basic_publish(exchange='zach_d',routing_key="".join(sys.argv[1:2]),body=msg,)
print(" [x] Sent {}".format(msg))

connection.close()

