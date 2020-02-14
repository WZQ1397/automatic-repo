# -*- coding: utf-8 -*-
# Author: Zach.Wang
# @Time  : 2019-12-26 16:16
def calculate_distance(first,second):
  return abs(first[0]-second[0]) + abs(first[1]-second[1])

def get_check_point(check_point_num):
  check_point_list=[]
  for values in range(check_point_num):
    check_point_list.append(eval(input().replace(' ',',')))
  return check_point_list

check_point_num=eval(input())
count = 2
# marathon_point_list=get_check_point(check_point_num)
marathon_point_list=[(0, 0), (8, 3), (11, -1), (10, 0),(7,3),(12,5)]
marathon_distance_dict=[]
marathon_skip_distance_dict={}
marathon_short_distance_dict=[]

# TODO get total full distance
# for values in range(check_point_num-1):
#   marathon_distance_list.append(calculate_distance(marathon_point_list[values],marathon_point_list[values+1]))

for first in range(check_point_num-1):
  marathon_distance_dict.append(calculate_distance(marathon_point_list[first],marathon_point_list[first+1]))

print(marathon_distance_dict)

for sec in range(check_point_num-2):
  for sec_end in range(sec+2,min(sec+count+2,check_point_num)):
    marathon_skip_distance_dict[str(sec)+':'+str(sec_end)]=calculate_distance(marathon_point_list[sec],marathon_point_list[sec_end])
    print(sec,sec_end,marathon_skip_distance_dict)

for k,v in marathon_skip_distance_dict.items():
  end = int(k.split(':')[-1])
  tracelist = marathon_distance_dict.copy()
  del tracelist[end-1]
  tracelist.append(v)
  for sub_end in range(end+2,check_point_num):
    print(str(sub_end-2)+":"+str(sub_end))
    tracelist.append(marathon_skip_distance_dict[str(sub_end-2)+":"+str(sub_end)])
    marathon_short_distance_dict.append(tracelist)
    del tracelist[sub_end-1]

????


print(marathon_short_distance_dict)
# print(marathon_short_distance_dict[min(marathon_short_distance_dict)])