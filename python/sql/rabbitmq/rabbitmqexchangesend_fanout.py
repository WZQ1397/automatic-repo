# python day 19
# author zach.wang
# -*- coding:utf-8 -*-
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange="zach",type="fanout")
for i in range(10):
    channel.basic_publish(exchange='zach',routing_key='',body='5lxyc2!',)
print(" [x] Sent 'Hello World!'")

connection.close()

