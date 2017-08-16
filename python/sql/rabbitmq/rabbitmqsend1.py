# python day 19
# author zach.wang
# -*- coding:utf-8 -*-
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

#消息持久化
channel.queue_declare(queue='zach',durable=True)
#发布消息
for i in range(10):
    channel.basic_publish(exchange='',routing_key='zach',body='5lxyc!',
                          properties=pika.BasicProperties(delivery_mode=2,))
print(" [x] Sent 'Hello World!'")

connection.close()

