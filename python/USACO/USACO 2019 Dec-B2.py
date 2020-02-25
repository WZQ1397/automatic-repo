# -*- coding: utf-8 -*-
# Author: Zach.Wang
# @Time  : 2019-12-25 19:09

factorynums=eval(input())
factoryroute=[]
for _ in range(factorynums-1):
  factoryroute.append(eval(input().replace(' ',',')))
print(factoryroute)
factoryroutereachcount={}

#TODO star situtation
def star_condition():
  for i in range(factorynums):
    factoryroutereachcount[i+1] = 0
  for route in factoryroute:
    factoryroutereachcount[route[0]] = factoryroutereachcount[route[0]] + 1
    factoryroutereachcount[route[1]] = factoryroutereachcount[route[1]] +1

  print(factoryroutereachcount)
  for i,v in factoryroutereachcount.items():
    if v == factorynums - 1:
      print(i)

#TODO B2
def node_condition():
  inbond, outbond=[0 for _ in range(factorynums+1)],[0 for _ in range(factorynums+1)]
  for node in factoryroute:
    # print(node[0],node[1])
    outbond[node[0]] += 1
    inbond[node[1]] += 1
  # print(outbond,inbond)
  vaild_node=-1
  for i in range(1,factorynums):
    if outbond[i] == 0 and vaild_node != -1:
      vaild_node = -1
      break
    if outbond[i] == 0:
      vaild_node = i
    # print(vaild_node)
  # print(inbond,outbond)
  print(vaild_node)

node_condition()
