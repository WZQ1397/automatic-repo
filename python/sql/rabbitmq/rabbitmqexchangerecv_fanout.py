# python day 19
# author zach.wang
# -*- coding:utf-8 -*-
import pika
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='zach',exchange_type='fanout')
res = channel.queue_declare(exclusive=False)
Qname = res.method.queue
channel.queue_bind(exchange="zach",queue=Qname)

def callback(ch, method, properties, body):
    tmp = body.decode()
    print(" [x] Received %s" % tmp)
#Qname!!!
channel.basic_consume(callback,
                      queue=Qname,
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

