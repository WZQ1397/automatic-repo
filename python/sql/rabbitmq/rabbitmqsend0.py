# python day 19
# author zach.wang
# -*- coding:utf-8 -*-
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')
channel.queue_declare(queue='hello zach')
#发布消息
for i in range(10):
    channel.basic_publish(exchange='',routing_key='hello',body='this is zach server!')
    channel.basic_publish(exchange='',routing_key='hello zach',body='5lxyc!')
print(" [x] Sent 'Hello World!'")

connection.close()

