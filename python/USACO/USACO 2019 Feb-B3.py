# -*- coding: utf-8 -*-
# Author: Zach.Wang
# @Time  : 2019-12-26 12:32


def get_check_point(check_point_num):
  check_point_list=[]
  for values in range(check_point_num):
    check_point_list.append(eval(input().replace(' ',',')))
  return check_point_list

check_point_num=eval(input())
traffic_list=[('on',1,1),('none', 10,14),('none',11,15),('off', 2 ,3)]

left,right = -999999999,99999999
for values in traffic_list:
  if values[0] == 'none':
    left = values[1] if values[1] > left else left
    right = values[-1]  if values[-1] < right else right
  if values[0] == 'off':
    left += values[1]
    right += values[-1]
  if values[0] == 'on':
    left -= values[-1]
    right -= values[1]
    left = max(0,left)


print(left,right)

