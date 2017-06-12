# python day 23
# author zach.wang
# -*- coding:utf-8 -*-
import platform,subprocess,re

class platfrominfo(object):
    def get_platform(self):
        '''获取操作系统名称及版本号'''
        return platform.platform()

    def get_version(self):
        '''获取操作系统版本号'''
        return platform.version()

    def get_architecture(self):
        '''获取操作系统的位数'''
        return platform.architecture()

    def get_machine(self):
        '''计算机类型'''
        return platform.machine()

    def get_node(self):
        '''计算机的网络名称'''
        return platform.node()

    def get_processor(self):
        '''计算机处理器信息'''
        return platform.processor()

    def get_system(self):
        '''获取操作系统类型'''
        return platform.system()

    def get_uname(self):
        '''汇总信息'''
        return platform.uname()

    def get_python_build(self):
        ''' the Python build number and date as strings'''
        return platform.python_build()

    def get_python_compiler(self):
        '''Returns a string identifying the compiler used for compiling Python'''
        return platform.python_compiler()

    def get_python_branch(self):
        '''Returns a string identifying the Python implementation SCM branch'''
        return platform.python_branch()

    def get_python_implementation(self):
        '''Returns a string identifying the Python implementation. Possible return values are: ‘CPython’, ‘IronPython’, ‘Jython’, ‘PyPy’.'''
        return platform.python_implementation()

    def get_python_version(self):
        '''Returns the Python version as string 'major.minor.patchlevel'
        '''
        return platform.python_version()

    def get_python_revision(self):
        '''Returns a string identifying the Python implementation SCM revision.'''
        return platform.python_revision()

    def get_python_version_tuple(self):
        '''Returns the Python version as tuple (major, minor, patchlevel) of strings'''
        return platform.python_version_tuple()

    def show_python_all_info(self):
        '''打印python的全部信息'''
        print('The Python build number and date as strings : [{}]'.format(get_python_build()))
        print('Returns a string identifying the compiler used for compiling Python : [{}]'.format(get_python_compiler()))
        print('Returns a string identifying the Python implementation SCM branch : [{}]'.format(get_python_branch()))
        print('Returns a string identifying the Python implementation : [{}]'.format(get_python_implementation()))
        print('The version of Python ： [{}]'.format(get_python_version()))
        print('Python implementation SCM revision : [{}]'.format(get_python_revision()))
        print('Python version as tuple : [{}]'.format(get_python_version_tuple()))

    def show_os_all_info(self):
        '''打印os的全部信息'''
        return self.get_uname()

    def show_os_info(self):
        '''打印os的全部信息'''
        print('操作系统信息:')
        print('获取操作系统名称及版本号 : [{}]'.format(self.get_platform()))
        print('获取操作系统版本号 : [{}]'.format(self.get_version()))
        print('获取操作系统的位数 : [{}]'.format(self.get_architecture()))
        print('计算机类型 : [{}]'.format(self.get_machine()))
        print('计算机的网络名称 : [{}]'.format(self.get_node()))
        print('计算机处理器信息 : [{}]'.format(self.get_processor()))
        print('获取操作系统类型 : [{}]'.format(self.get_system()))
        print('汇总信息 : [{}]'.format(self.get_uname()))

def showinfo():
    return platfrominfo().show_os_all_info()

def sys_version():
    subprocess.getstatusoutput('wmic cpu list brief')
    '''
    info = ""
    infodic = {}
    with open("info.txt","r") as f:
        info = "".join(f.readlines())
    judge = re.compile(r'\n')
    info = judge.split(info)
    judge2 = re.compile(r':')
    for var in info:
        if judge2.split(str(var))[0] == "登录服务器":
            break
        print(judge2.split(str(var)))

    info = judge2.split(info)
    '''
    Maohao = re.compile(r':')
    Jinghao = re.compile(r'#')
    Blank = re.compile(r'\s+')
    '''
    Cpu = Maohao.split(re.sub("\s+",":",str(list(re.compile(r'\(R\) ').\
            split(str(list(subprocess.getstatusoutput('wmic cpu list brief')))))[0])))[-1],\
                list(re.compile(r'Socket').split(str(list(re.compile(r'\(R\) ').\
                              split(str(list(subprocess.getstatusoutput('wmic cpu list brief')))))[-1])))[0]
    PsyMem = int(list(Maohao.split(str(re.sub("\s+",":",Maohao.
                 split(re.sub("n",":",str(list(re.compile(r'Physical Memory Array ').\
    split(str(list(subprocess.getstatusoutput('wmic memphysical list brief')))))[0])))[-1]))))[0])/1048576

    VirtMem = list(Blank.split(str(list(Jinghao.split(
        re.sub("\n","#",str(list(
            subprocess.getstatusoutput('wmic pagefile list brief'))[-1]))))[-4]).strip()))
    print(VirtMem[-3],VirtMem[-1])
    '''

    disk = list(re.compile(r'\\n\\n').split(str(list(subprocess.getstatusoutput('wmic volume get name,freespace')))))[1:]
    for x in range(0,len(disk)-1):
        diskdetail = list(Blank.split(str(disk[x]).strip()))
        print("{} {:.2f}GB".format(diskdetail[1],int(str(diskdetail[0]))/(1024**3)))
    #IPv4 = list(Maohao.split(str(list(subprocess.getstatusoutput('ipconfig | findstr IPv4'))[-1])))[-1]
    #print(IPv4)

    '''
    dic = {}
    dic['Cpu'] = Cpu
    dic['PsyMem'] = PsyMem
    return dic
    '''


def win():
    sys_version()

win()