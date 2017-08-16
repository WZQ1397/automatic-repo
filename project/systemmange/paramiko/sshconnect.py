# python day 13
# author zach.wang
# -*- coding:utf-8 -*-
import paramiko

hostname = "172.16.6.226"
port = 22
username = 'root'
passwd = 'edong'
cmd = 'uptime'
ssh = paramiko.SSHClient()
# 允许连接不在know_hosts文件中的主机
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname,port,username,passwd)

stdin , stdout, stderr = ssh.exec_command(cmd)

res = stdout.read()
print(res.decode())
ssh.close()

