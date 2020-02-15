# -*- coding: utf-8 -*-
# Author: Zach.Wang
# @Time  : 2019-12-26 12:32

check_point_num=eval(input())
# blist=[(4,10,1),(8,13,3),(2,6,2)]
blist = []
for values in range(check_point_num):
  blist.append(eval(input().replace(' ',',')))
blist.sort()
blist_start_time,blist_end_time = [],{}
index = 0
for x in blist:
  blist_start_time.append(x[0])
  blist_end_time[index] = x[1]
  index+=1
print(blist_start_time,blist_end_time)
current_buckets = max_buckets = 0
count = 0
for buckets in blist:
  count += 1
  current_buckets+=buckets[-1]
  need_pop_list_of_blist_end_time=[]
  i = 0
  for ind,end in blist_end_time.items():
    if i >= count:
      break
    i += 1
    if buckets[0] > end and end > 0:
      current_buckets-=blist[ind][-1]
      blist_end_time[ind]=-1
  max_buckets = max_buckets if max_buckets > current_buckets else current_buckets
  print(max_buckets)








