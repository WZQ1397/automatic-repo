# python day 19
# author zach.wang
# -*- coding:utf-8 -*-
import pika,sys
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='zach_d',exchange_type='direct')
res = channel.queue_declare(exclusive=False)
Qname = res.method.queue
routings = sys.argv[1:]
if len(routings) < 1:
    sys.stdout.write("args error!")
    routings = ['info']

for r in routings:
    print(r)
    channel.queue_bind(exchange="zach_d",queue=Qname,routing_key=r)

def callback(ch, method, properties, body):
    tmp = body.decode()
    print(" [x] Received %s" % tmp)
#Qname!!!
channel.basic_consume(callback,
                      queue=Qname,
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
try:
    channel.start_consuming()
except KeyboardInterrupt as e:
    print(e,"bye!")

