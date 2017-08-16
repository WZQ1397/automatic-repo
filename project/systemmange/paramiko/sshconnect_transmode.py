# python day 13
# author zach.wang
# -*- coding:utf-8 -*-
import paramiko,os

hostname = "172.16.6.214"
port = 22
username = 'root'
passwd = 'edong.com'
cmd = 'uptime'

key = 'id_rsa_2048'
sshtype = 0
if os.path.exists(key) is True:
    print(os.path.exists(key))
    private_key = paramiko.RSAKey.from_private_key_file(key)
    trans_mode = paramiko.Transport((hostname,port))
    trans_mode.connect(username=username,password=passwd,pkey=private_key)
    ssh = paramiko.SSHClient()
    ssh._transport = trans_mode
    sshtype = 1
else:
    ssh = paramiko.SSHClient()
    #FIXME paramiko.AutoAddPolicy / paramiko.RejectPolicy
    ssh.set_missing_host_key_policy(paramiko.WarningPolicy())
    ssh.connect(hostname,port,username,passwd)

stdin , stdout, stderr = ssh.exec_command(cmd)
res = stdout.read()
print(res.decode())
ssh.close()

