# -*- coding: utf-8 -*-
# Author: Zach.Wang
# @Time  : 2019-12-26 12:32


cow_pos=[7,8,9]
pos=True
def get_free_positions():
  cow_pos.sort()
  if (cow_pos[-1] - cow_pos[1]) >1 and (cow_pos[1] - cow_pos[0]) > 1:
    if (cow_pos[-1] - cow_pos[1]) > (cow_pos[1] - cow_pos[0]):
      step = 2 if (cow_pos[1] - cow_pos[0]) > 2 else 1
      cow_pos[-1] = cow_pos[1]-step
    else:
      step = 2 if (cow_pos[-1] - cow_pos[1]) > 2 else 1
      cow_pos[0] = cow_pos[1]+step
  else:
    if (cow_pos[-1] - cow_pos[1]) == (cow_pos[1] - cow_pos[0]):
      return False
    else:
      if (cow_pos[-1] - cow_pos[1]) == 1:
        step = 2 if (cow_pos[1] - cow_pos[0]) > 2 else 1
        cow_pos[-1]=cow_pos[1]-step
      if (cow_pos[1] - cow_pos[0]) == 1:
        step = 2 if (cow_pos[-1] - cow_pos[1]) > 2 else 1
        cow_pos[0]=cow_pos[1]+step
  print(cow_pos)
  return True

flag = True
while flag:
  flag = get_free_positions()


# zachcowpos=[4,7,9]
# zachcowpos.sort()
# min_move = 0 if zachcowpos[-1] == zachcowpos[0] + 2 else 1 if zachcowpos[-1] == zachcowpos[1] + 2 or zachcowpos[1] == zachcowpos[0] + 2 else 2
# max_move = max(zachcowpos[-1]-zachcowpos[-2],zachcowpos[1]-zachcowpos[0])-1
# print(min_move,max_move)
