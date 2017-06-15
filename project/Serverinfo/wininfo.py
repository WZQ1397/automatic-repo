# python day 24
# author zach.wang
# -*- coding:utf-8 -*-

import subprocess,socket,time,platform

def win_agent_serv_info():
    wininfo = {}
    wininfo['Cpu'] = subprocess.getstatusoutput('wmic cpu list brief')

    wininfo['PsyMem'] = subprocess.getstatusoutput('wmic memphysical list brief')

    wininfo['VirtMem'] =subprocess.getstatusoutput('wmic pagefile list brief')

    wininfo['disk'] = subprocess.getstatusoutput('wmic volume get name,freespace')

    wininfo['IPv4'] = subprocess.getstatusoutput('ipconfig | findstr IPv4')

    return wininfo

class platforminfo(object):
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
        print('The Python build number and date as strings : [{}]'.format(self.get_python_build()))
        print('Returns a string identifying the compiler used for compiling Python : [{}]'.format(self.get_python_compiler()))
        print('Returns a string identifying the Python implementation SCM branch : [{}]'.format(self.get_python_branch()))
        print('Returns a string identifying the Python implementation : [{}]'.format(self.get_python_implementation()))
        print('The version of Python ： [{}]'.format(self.get_python_version()))
        print('Python implementation SCM revision : [{}]'.format(self.get_python_revision()))
        print('Python version as tuple : [{}]'.format(self.get_python_version_tuple()))

    def show_os_all_info(self):
        '''打印os的全部信息'''

        return '''
        操作系统信息:
        获取操作系统名称及版本号 : [{}]
        获取操作系统版本号 : [{}]
        获取操作系统的位数 : [{}]
        计算机类型 : [{}]'.format())
        计算机的网络名称 : [{}]
        计算机处理器信息 : [{}]
        获取操作系统类型 : [{}]
        '''.format(self.get_platform(),self.get_version(),self.get_architecture(),self.get_machine(),
                   self.get_node(),self.get_processor(),self.get_system())

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
    return platforminfo().show_os_all_info()

def sendbasicinfo():
    sk = socket.socket()
    ip=("127.0.0.1",8888)
    sk.connect(ip)
    skreply = sk.recv(1000)
    print(skreply.decode())
    count = 0
    msg = showinfo()
    count += 1
    sk.sendall(str(msg).encode())
    skreply = sk.recv(1024)
    print(skreply.decode())
    if msg == "bye":
        sk.close()

def sendadvinfo():
    sk = socket.socket()
    ip=("127.0.0.1",8888)
    sk.connect(ip)
    skreply = sk.recv(1000)
    print(skreply.decode())
    count = 0
    msg = win_agent_serv_info()
    count += 1
    sk.sendall(str(msg).encode())
    skreply = sk.recv(1024)
    print(skreply.decode())
    if msg == "bye":
        sk.close()

#sendbasicinfo()
time.sleep(1)
sendadvinfo()