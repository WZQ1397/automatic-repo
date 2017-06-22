# python day 26
# author zach.wang
# -*- coding:utf-8 -*-
import warnings

zach = warnings.warn
def warning_on_one_line(message, category, filename, lineno,
                        file=None, line=None):
    return '-> {}:{}: {}:{}'.format(
        filename, lineno, 'Zach', message)

zach('Warning message')
warnings.formatwarning = warning_on_one_line
zach('Warning message')