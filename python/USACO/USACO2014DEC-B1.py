# -*- coding: utf-8 -*-
# Author: Zach.Wang
# @Time  : 2019-12-26 10:24

def calculate_distance(first,second):
  return abs(first[0]-second[0]) + abs(first[1]-second[1])

def get_check_point(check_point_num):
  check_point_list=[]
  for values in range(check_point_num):
    check_point_list.append(eval(input().replace(' ',',')))
  return check_point_list

check_point_num=eval(input())
# marathon_point_list=get_check_point(check_point_num)
marathon_point_list=[(0, 0), (8, 3), (11, -1), (10, 0), (17,3)]
marathon_distance_dict=[]
marathon_skip_distance_dict={}
marathon_short_distance_dict={}

# TODO get total full distance
# for values in range(check_point_num-1):
#   marathon_distance_list.append(calculate_distance(marathon_point_list[values],marathon_point_list[values+1]))

for first in range(check_point_num-1):
  marathon_distance_dict.append(calculate_distance(marathon_point_list[first],marathon_point_list[first+1]))

# print(marathon_distance_dict)

for sec in range(check_point_num-2):
  marathon_skip_distance_dict[str(sec)+':'+str(sec+2)]=calculate_distance(marathon_point_list[sec],marathon_point_list[sec+2])
# print(marathon_skip_distance_dict)

for k,v in marathon_skip_distance_dict.items():
  first_end ,sec_start = int(k.split(':')[0]),int(k.split(':')[-1])
  marathon_short_distance_dict['skip-'+k] = v
  for v in marathon_distance_dict[:first_end]:
    marathon_short_distance_dict['skip-'+k] += v
  for v in marathon_distance_dict[sec_start:]:
    marathon_short_distance_dict['skip-'+k] += v

print(marathon_short_distance_dict)
print(marathon_short_distance_dict[min(marathon_short_distance_dict)])

