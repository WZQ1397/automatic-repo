
import numpy as np
import matplotlib.pylab as plt

predict2020_value_list=[]
predict_year = 2020
# 使用最小二乘法生成公式 一元线性回归模型
def least_square(x, y):
  # 获取多项式个数
  n = len(x)
  sumX, sumY, sumXY, sumXX = 0, 0, 0, 0
  # 生成各个segma的模块
  for i in range(0, n):
    sumX += x[i]
    sumY += y[i]
    sumXX += x[i] * x[i]
    sumXY += x[i] * y[i]
  mean_x = sumX / n
  mean_y = sumY / n
  # 建立模型
  a = (n * sumXY - sumX * sumY) / (n * sumXX - sumX * sumX)
  b = mean_y - a * mean_x
  return a, b

def figure_drawing(month, values, fig_num, **kwargs):
  '''

  :param month:  2020年1-12月
  :param values:  预测汇率值
  :param fig_num:  设置精准数
  :param kwargs:   传入plot属性设置字典
  :return:
  '''

  # 编号为1的图
  f = plt.figure(fig_num)
  # 1×1 网格，第一子图 只设置一个图
  ax = f.add_subplot(111)

  # 设置上限，下限，标签名和X,Y轴线值
  ylimit_down = kwargs['ylimit_down']
  ylimit_up = kwargs['ylimit_up']
  xlabel = kwargs['xlabel']
  ylabel = kwargs['ylabel']
  xticks = kwargs['xticks']
  yticks = kwargs['yticks']

  # 应用上限，下限，标签名和X,Y轴线值
  ax.scatter(month, values, s=10, c='r')
  ax.set_xlabel(xlabel)
  ax.set_ylabel(ylabel)
  ax.set_yticks(yticks)
  ax.set_xticks(xticks)

  # 设置标题
  title = kwargs['title'] + '\n'
  ax.set_title(title)

  # 绘制数据点和折线图
  plt.setp(ax.xaxis.get_majorticklabels(), rotation=-30)
  plt.plot(month, values, 'm.-.', label='Rate', linewidth=1)

  # 查找最低点并标出
  lowest = values.index(min(values))+1
  plt.axvline(lowest, linestyle='-', color='purple', label="Lowest:%i " % lowest)

  # 设置网格和框架
  legend = ax.legend(loc="upper left")
  legend_f = legend.get_frame()

  # 设置指示标志背景为绿色
  legend_f.set_facecolor("green")

  # 设置上下限
  plt.axhline(ylimit_down, linestyle=':', color='brown')
  plt.axhline(ylimit_up, linestyle=':', color='darkblue')

  # 绘制网格
  plt.grid(True)


if __name__ == "__main__":
    # 年份生成器
    xyear = [years for years in range(2010,2020)]
    # print(xyear)
    # 二维汇率数组 yvalue[month][year]
    yvalue = [[9.6218, 8.9195, 8.1979, 8.3312, 8.2489, 7.2819, 7.0896, 7.3739, 7.8131, 7.7795],
              [9.3832, 9.0531, 8.3202, 8.2832, 8.3293, 7.0357, 7.1254, 7.3458, 7.7625, 7.6393],
              [9.2618, 9.1741, 8.3957, 8.0454, 8.5170, 6.8335, 7.2320, 7.3013, 7.7264, 7.5729],
              [9.1500, 9.4445, 8.3836, 8.0368, 8.6198, 6.8092, 7.3774, 7.4265, 7.6900, 7.5407],
              [8.7533, 9.4747, 8.1134, 8.0468, 8.5982, 6.8853, 7.3711, 7.5862, 7.5721, 7.6398],
              [8.3500, 9.3520, 7.9582, 7.9362, 8.5059, 6.8590, 7.3549, 7.7030, 7.6180, 7.7596],
              [8.5686, 9.3195, 7.9394, 8.0685, 8.3804, 6.8647, 7.3982, 7.8553, 7.8423, 7.7164],
              [8.7422, 9.2067, 7.9037, 8.1221, 8.1676, 6.9822, 7.4365, 7.9062, 7.9414, 7.7465],
              [8.8806, 8.8593, 8.0341, 8.1902, 7.9128, 7.1273, 7.4773, 7.8542, 7.9476, 7.8275],
              [9.2132, 8.6571, 8.0787, 8.2794, 7.7044, 7.0281, 7.4676, 7.7962, 7.9328, 7.8220],
              [8.9845, 8.6912, 8.0839, 8.2803, 7.6504, 6.8630, 7.3666, 7.8004, 7.8856, 7.7992],
              [8.7384, 8.3608, 8.1525, 8.3004, 7.5799, 6.9073, 7.2970, 7.8372, 7.8818, 7.7576]]

    # 生成每个月的趋势预计公式
    for months in range(1, 13):
      a, b = least_square(xyear, yvalue[months - 1])
      # print("%i month ==> y = %10.5fx + %10.5f" % (months, a, b))
      predict2020_value_list.append(round(a * predict_year + b,4))

    # print(predict_year, 'values:', predict2020_value_list)

    fig_opt = {
        'title':  '2020 Year Exchange rate forecast ',
        'xlabel': '2020 months',
        'ylabel': 'Exchange rate',
        'ylimit_down': 7,
        'ylimit_up': 8.6,
        'ytick_down': 6.5,
        'ytick_up': 10,
        'xticks': np.arange(1,13, 1),
        'yticks': np.arange(7, 9, 0.2),
    }

    # 生成图片
    figure_drawing([month for month in range(1,13)], predict2020_value_list, 1, **fig_opt)
    plt.show()

    range_excharge = eval(input("请输入一个月份[1-12]："))
    # 判断用户输入是否合法
    assert 1 <= range_excharge <= 12, '[Error] [%s] is not a valid month' % range_excharge
    # 找出范围内的最低值
    predict2020_value_list_range = predict2020_value_list[:range_excharge]
    lowest = predict2020_value_list_range.index(min(predict2020_value_list_range)) + 1
    print("从2020年1月至旅行出发时，建议在{0}月换汇，汇率较低\n最好的换汇时间是{0}月 ==> 汇率：{1:.5f}"
          .format(lowest, predict2020_value_list_range[lowest - 1]))