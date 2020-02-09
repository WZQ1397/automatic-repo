# -*- coding: utf-8 -*-
# Author: Zach.Wang
# @Time  : 2019-12-24 16:10

predict2020_value_list=[6.961153333332845,
                        6.882159999997782,
                        6.84168666666892,
                        6.869866666668145,
                        7.013566666669362,
                        7.2024000000003525,
                        7.2634200000021,
                        7.31390666666465,
                        7.3549733333350105,
                        7.260779999999784,
                        7.232080000001247,
                        7.299973333334833]

range_excharge = eval(input("请输入一个月份[1-12]："))
# 判断用户输入是否合法
assert 1<=range_excharge<=12, '[Error] [%s] is not a valid month' % range_excharge
# 找出范围内的最低值
predict2020_value_list_range = predict2020_value_list[:range_excharge]
lowest = predict2020_value_list_range.index(min(predict2020_value_list_range)) + 1
print("从2020年1月至旅行出发时，建议在{0}月换汇，汇率较低\n最好的换汇时间是{0}月 ==> 汇率：{1:.5f}"
      .format(lowest,predict2020_value_list_range[lowest-1]))


