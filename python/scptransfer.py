import paramiko
import os
import sys
import getpass
print("\033[32;1m****开始配置目标机器信息*****\033[0m")
#ips = input("主机IP:")
#user = input("主机账号:")
#password = getpass.getpass("主机密码:")
#port = 22
user = "root"
ips = "10.10.123.96"
password = "B^Dc%4LSBvhZZK3B"
port = 22
class Tools(object):
    def __init__(self, user, password, port, ips):
        self.user = user
        self.password = password
        self.port = port
        self.ip = ips
    def connect(self):
        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(self.ip, self.port, self.user, self.password)
            print("连接已建立")
        except Exception as e:
            print("未能连接到主机")
    def cmd(self):
        cmd = input("请输入要执行的命令:>>")
        stdout, stdin, stderr = self.ssh.exec_command(cmd)
        #print(sys.stdout.read())
    def input(self):
        self.local_file_abs = input("本地文件的绝对路径:>>")
        self.remote_file_abs = input("远程文件的绝对路径:>>")
    def put(self):
        sftp = paramiko.SFTPClient.from_transport(self.ssh.get_transport())
        sftp = self.ssh.open_sftp()
        self.input()
        sftp.put(self.local_file_abs,self.remote_file_abs)
    def get(self):
        sftp = paramiko.SFTPClient.from_transport(self.ssh.get_transport())
        sftp = self.ssh.open_sftp()
        self.input()
        sftp.get(self.remote_file_abs,self.local_file_abs)
    def close(self):
        self.ssh.close()
        print("连接关闭")
obj = Tools(user, password, port, ips)
if __name__ == "__main__":
    msg = '''\033[32;1m
    执行命令 >>输入cmd
    上传文件 >>输入put
    下载文件 >>输入get
    退出     >>输入q\033[0m
    '''
    getattr(obj, "connect")()
    while True:
        print(msg)
        inp = input("action:>>")
        if hasattr(obj,inp):
            getattr(obj,inp)()
        if inp == "q":
            getattr(obj,"close")()
            exit()
           else:print("没有该选项，请重新输入:>>")
