# -*- coding: utf-8 -*-
# Author: Zach.Wang
# @Time  : 2019-12-26 12:32
# FIXME NOT GOOD ANSWER
# MAX_CARRY=2
# ARRIVE_TIME=[1,1,10,14,4,3]

MAX_CARRY=eval(input())
ARRIVE_TIME=list(eval(input().replace(' ',',')))
ARRIVE_TIME.sort(reverse=True)
print(ARRIVE_TIME)
count,max_wait = 0,0
flag = True
while flag or ARRIVE_TIME != []:
  current_max_wait = max(ARRIVE_TIME[-MAX_CARRY:])-min(ARRIVE_TIME[-MAX_CARRY:])
  print(current_max_wait)
  max_wait = max_wait if current_max_wait < max_wait else current_max_wait
  for _ in range(MAX_CARRY):
    try:
      ARRIVE_TIME.pop()
    except Exception as e:
      flag = False
  if ARRIVE_TIME == []:
    flag = False

print(max_wait)