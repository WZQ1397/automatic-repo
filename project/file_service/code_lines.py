#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import prettytable as pt

# 后缀集合
CPP_SUFFIX_SET = {'.h', '.hpp', '.hxx', '.c', '.cpp', '.cc', '.cxx'}
PYTHON_SUFFIX_SET = {'.py'}
JAVA_SUFFIX_SET = {'.java'}
HTML_SUFFIX_SET = {'.htm','.html'}

# 全局变量
cpp_lines = 0
python_lines = 0
java_lines = 0
html_lines = 0
total_lines = 0


def list_files(path):
    '''
    遍历工程路径path，如果遇到文件则统计其行数，如果遇到目录则进行递归
    '''
    filenames = os.listdir(path)
    for f in filenames:
        fpath = os.path.join(path, f)
        if (os.path.isfile(fpath)):
            count_lines(fpath)
        if (os.path.isdir(fpath)):
            list_files(fpath)


def count_lines(fpath):
    '''
    对于文件fpath，计算它的行数，然后根据其后缀将它的行数加到相应的全局变量当中
    '''
    global CPP_SUFFIX_SET, PYTHON_SUFFIX_SET, JAVA_SUFFIX_SET, HTML_SUFFIX_SET
    global cpp_lines, python_lines, java_lines, html_lines, total_lines

    # 统计行数
    with open(fpath, 'rb') as f:
        cnt = 0
        last_data = '\n'
        while True:
            data = f.read(0x400000)
            if not data:
                break
            cnt += data.count(b'\n')
            last_data = data
        if last_data[-1:] != b'\n':
            cnt += 1

    # 只统计C/C++，Python和Java这三类代码
    suffix = os.path.splitext(fpath)[-1]
    if suffix in CPP_SUFFIX_SET:
        cpp_lines += cnt
    elif suffix in PYTHON_SUFFIX_SET:
        python_lines += cnt
    elif suffix in JAVA_SUFFIX_SET:
        java_lines += cnt
    elif suffix in HTML_SUFFIX_SET:
        html_lines += cnt
    else:
        pass


def print_result():
    '''
    本函数依赖库prettytable，请使用sudo pip3 install prettytable进行安装
    '''
    tb = pt.PrettyTable()
    tb.field_names = ['CPP', 'PYTHON', 'JAVA', 'HTML', 'TOTAL']
    tb.add_row([cpp_lines, python_lines, java_lines, html_lines, total_lines])
    print(tb)


if __name__ == '__main__':
    if (len(sys.argv) != 2):
        print("Usage : python3 code_analyst.py project_path")
    else:
        project_path = sys.argv[1]
        list_files(project_path)

        total_lines = cpp_lines + python_lines + java_lines + html_lines
        print_result()
