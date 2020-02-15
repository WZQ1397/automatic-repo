# -*- coding: utf-8 -*-
# Author: Zach.Wang
# @Time  : 2019-12-26 12:32

mixmilk=[[10,3],[11,4],[12,5]]
milk_count = len(mixmilk)
for count in range(100):
  cow_old_id=count % milk_count
  cow_new_id=0 if cow_old_id == milk_count-1 else cow_old_id+1
  old = mixmilk[cow_old_id][1]
  new = mixmilk[cow_new_id][1]
  if old + new > mixmilk[cow_new_id][0]:
    new = mixmilk[cow_new_id][0]
    old = old - new
    mixmilk[cow_new_id][1]=new
    mixmilk[cow_old_id][1]=old
  else:
    new = mixmilk[cow_new_id][1] + mixmilk[cow_old_id][1]
    old = 0
    mixmilk[cow_new_id][1]=new
    mixmilk[cow_old_id][1]=old
  # print(new,old)
print(mixmilk)

