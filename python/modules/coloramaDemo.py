# -*- coding: utf-8 -*-
# Author: Zach.Wang
# @Time  : 2020-03-31 9:18

from colorama import init, Fore, Back, Style

if __name__ == "__main__":
  init(autoreset=True)  # 初始化，并且设置颜色设置自动恢复
  print(Fore.RED + 'some red text')
  aaa= Back.GREEN
  print(aaa + 'and with a green background')
  print(Style.DIM + 'and in dim text')
  # 如果未设置autoreset=True，需要使用如下代码重置终端颜色为初始设置
  # print(Fore.RESET + Back.RESET + Style.RESET_ALL)  autoreset=True
  print('back to normal now')