# python day 19
# author zach.wang
# -*- coding:utf-8 -*-
import pika,time

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

#channel.queue_declare(queue='hello')

def callback(ch, method, properties, body):
    tmp = body.decode()
    #print(ch, method, properties)
    print(" [x] Received %s" % tmp)
    time.sleep(0.5)
    channel.basic_ack(delivery_tag=method.delivery_tag)

#公平调度
channel.basic_qos(prefetch_count=1)

#作为接收
channel.basic_consume(callback,
                      queue='hello',
                      no_ack=False)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

