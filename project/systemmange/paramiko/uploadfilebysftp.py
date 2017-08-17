# python day 13
# author zach.wang
# -*- coding:utf-8 -*-
import paramiko

private_key = paramiko.RSAKey.from_private_key_file('id_rsa_2048')

hostname = "172.16.6.214"
port = 22
username = 'root'
passwd = 'edong.com'
cmd = 'ls /home'
remote_target = '/home/iplist.bin'
local_target = 'iplist.bin'
trans_mode = paramiko.Transport((hostname,port))
trans_mode.connect(username=username,password=passwd)
sftp = paramiko.SFTPClient.from_transport(trans_mode)
sftp.put(local_target,remote_target)
#sftp.get(remote_target,local_target)
#FIXME more method https://github.com/paramiko/paramiko/
ssh = paramiko.SSHClient()
ssh._transport = trans_mode
stdin , stdout, stderr = ssh.exec_command(cmd)
res = stdout.read()
print(res.decode())
trans_mode.close()
