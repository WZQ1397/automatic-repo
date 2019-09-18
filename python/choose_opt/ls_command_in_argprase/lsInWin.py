# 颜色语法： \033[显示方式;前景色;背景色m 这种方法在windows cmd中不适用
import os
import argparse
import datetime
from wincmd_color import *
# import win32com.client

# 获取快捷方式文件的原地址
# shell = win32com.client.Dispatch("WScript.Shell")
# shortcut = shell.CreateShortCut("ls.py-lnk.lnk")
# print(shortcut.Targetpath)

FILE_TYPE = {
    'dir': '\\',
    'exe': '*',
    'lnk': '@',
}

DETAIL_HEADER = '{:<15}\t{:<15}\t{:<8}\t{}'.format('创建时间', '修改时间', '文件大小', '文件名')
FILE_DETAIL_FORMAT = '{create_time:<20}\t{modify_time:<20}\t{file_size:<10}\t{file_name}'

class ShowFile:
    '''
    show file with color, use classmethod and class to functionize
    '''
    # 文件夹, 蓝色
    @classmethod
    def show_directory(cls,message):
        FOREGROUND_DARK_SKYBLUE(message)()


    # exe文件, 红色
    @classmethod
    def show_exe_file(cls, message):
        FOREGROUND_RED(message)()

    # py文件 黄色
    @classmethod
    def show_py_file(cls, message):
        YellowBlue(message)()


    # 隐藏文件 绿色
    @classmethod
    def show_hide_file(cls, message):
        FOREGROUND_DARK_GREEN(message)()

    # lnk文件 天蓝色
    @classmethod
    def show_lnk_file(cls, message):
        FOREGROUND_YELLOW(message)()

    @classmethod
    def show_normal_file(cls, message):
        FOREGROUND_BOLDBLACK(message)()

class LsCommand:
    def __init__(self, show_all=False, directory='.', end='\t', add_file_type=False, show_detail=False, recursion=False, shortcut=False):
        '''
        :param show_all: option -a
        :param directory: option -d
        :param end: option -l / -C
        :param add_file_type: option -F
        :param show_detail: option -S
        :param recursion: option -R
        :param shortcut: option -shortcut
        '''
        self.show_all = show_all
        self.directory = directory
        self.end = end
        self.add_file_type = add_file_type
        self.show_detail = show_detail
        self.recursion = recursion
        self.shortcut = shortcut
        if self.show_detail:
            print(DETAIL_HEADER)
            self.end = '\n'
        if self.shortcut:
            self.add_file_type = False

    def get_message(self, file, prefix=''):
        file_name = os.path.basename(file)
        if not self.show_detail:
            return file_name

        # 查看文件状态信息
        stat_result = os.stat(file)

        UnitList=['K','M','G','T']
        # 计算文件大小
        UnitIndex=0
        file_size = stat_result.st_size/1024
        while file_size > 1024:
            file_size/=1024
            UnitIndex+=1

        message = FILE_DETAIL_FORMAT.format(**{
            'create_time' : datetime.datetime.fromtimestamp(stat_result.st_ctime).strftime('%Y-%m-%d %H:%M'),
            'modify_time' : datetime.datetime.fromtimestamp(stat_result.st_mtime).strftime('%Y-%m-%d %H:%M'),
            'file_size' : str(round(file_size,3))+UnitList[UnitIndex],
            'file_name' : prefix + file_name
        })

        return message

    def get_lnk_file_source_path(self, path):
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(path)
        return shortcut.Targetpath

    def show_file_info(self, abs_path, prefix=''):

        file_type_str = ''
        file = os.path.basename(abs_path)
        message = self.get_message(abs_path, prefix)

        if os.path.isdir(abs_path):
            if self.add_file_type:
                file_type_str = FILE_TYPE.get('dir')
            ShowFile.show_directory(message + file_type_str + self.end)
        elif file.endswith('.exe'):
            if self.add_file_type:
                file_type_str = FILE_TYPE.get('exe')
            ShowFile.show_exe_file(message + file_type_str + self.end)
        elif file.startswith('.'):
            ShowFile.show_hide_file(message + self.end)
        elif file.endswith('.py'):
            ShowFile.show_py_file(message + self.end)
        elif file.endswith('.lnk'):
            if self.add_file_type:
                file_type_str = FILE_TYPE.get('lnk')

            if self.shortcut:
                source_abs_path = self.get_lnk_file_source_path(abs_path)
                ShowFile.show_lnk_file(message + file_type_str + ' -> ' + source_abs_path + '\n')
            else:
                ShowFile.show_lnk_file(message + file_type_str + self.end)
        else:
            ShowFile.show_normal_file(message + self.end)

    def handle_directory(self, path, grade=1, prefix='+'):
        if not os.path.exists(path):
            raise ValueError(f'{path} not exists')

        if not os.path.isdir(path):
            raise ValueError(f'{path} not a directory')

        add_grade = False
        for file in os.listdir(path):

            if not self.show_all:
                if file.startswith('.'):
                    continue

            abs_path = os.path.join(path, file)
            self.show_file_info(abs_path, prefix=grade * prefix + " ")
            if os.path.isdir(abs_path):
                if not add_grade:
                    grade += 1
                self.handle_directory(abs_path, grade=grade)

    def run(self):
        for file in os.listdir(self.directory):
            abs_path = os.path.join(self.directory, file)

            if not self.show_all:
               if file.startswith('.'):
                   continue

            self.show_file_info(abs_path)

            if self.recursion:
                if os.path.isdir(abs_path):
                    self.handle_directory(abs_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='ls', usage='显示文件夹下面的文件')
    # 添加可用选项， 当选项接受1个或者不需要参数时指定nargs='?',当没有参数时，会从default中取值。
    # nargs='+'也和nargs='*'一样，但是有一个区别当'+'时少于1个参数（没有参数）位置参数会报错误,而'*'会使用默认值

    parser.add_argument('-a', '--all', const=True, nargs='?', default=True, help='是否显示隐藏文件')
    #required: 当某个选项指定需要在命令中出现的时候用这个参数
    parser.add_argument('-d', '--directory', help='指定文件夹')

    # const=True 永远都是真的
    parser.add_argument('-l', const=True, nargs='?', help='单列显示，每个文件后面都换行')
    parser.add_argument('-C', const=True, nargs='?', help='多列显示，每个文件后面不换行, 这是默认值, 没有颜色')
    parser.add_argument('-F', const=True, nargs='?', help=r'在每个文件夹后追加类型表示符, *:exe文件, \:文件夹, @:快捷方式文件')
    parser.add_argument('-S', const=True, nargs='?', help='显示文件的详细信息')
    parser.add_argument('-R', const=True, nargs='?', help='递归显示子目录下面的文件信息')
    # choices: 这个参数用来检查输入参数的范围
    parser.add_argument('-shortcut', nargs='?',choices=[True,False], help='如果文件为快捷方式，显示出源文件地址')
    # 初始化选项方法
    arg = parser.parse_args()

    show_all = arg.all or False
    directory = arg.directory or '.'
    end = '\t'
    if arg.C:
        end = '\t'
    if arg.l:
        end = '\n'

    F = arg.F or False
    show_detail = arg.S or False

    recursion = arg.R or False
    shortcut = arg.shortcut or False

    ls = LsCommand(show_all=show_all, directory=directory, end=end, add_file_type=F, show_detail=show_detail, recursion=recursion, shortcut=shortcut)
    ls.run()
