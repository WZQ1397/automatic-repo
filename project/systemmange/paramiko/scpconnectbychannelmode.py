#!/usr/bin/env python
import paramiko
import os,sys,time
 
hostname="192.168.1.111"   # 远程主机
username="root"                    # 远程主机的用户名
password="SKJh935yft#"
 
blip="192.168.1.1"              # 堡垒机
bluser="root"                        #堡垒机用户名
blpasswd="SKJh935yft#"
 
tmpdir="/tmp"                   #  客户机源文件路径、堡垒机临时路劲和远程主机目标文件路径
remotedir="/data"             
localpath="/home/nginx_access.tar.gz"
tmppath=tmpdir+"/nginx_access.tar.gz"
remotepath=remotedir+"/nginx_access_hd.tar.gz"
 
port=22
passinfo='\'s password: '                     # 这是密码信息
paramiko.util.log_to_file('syslogin.log')   # paramiko自带的日志功能
 
t = paramiko.Transport((blip, port))           # 创建连接对象
t.connect(username=bluser, password=blpasswd)   #建立连接
sftp =paramiko.SFTPClient.from_transport(t)  # 创建SFTP连接
sftp.put(localpath, tmppath)    # 利用put方法上传文件
 
sftp.close()          # 关闭sftp连接
 
ssh=paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname=blip,username=bluser,password=blpasswd)

#TODO IMPORTANT TEMPLATE--------------
#创建一个新的会话
channel=ssh.invoke_shell()
channel.settimeout(10)
 
buff = ''
resp = ''

channel.send('scp '+tmppath+' '+username+'@'+hostname+':'+remotepath+'\n')
 
while not buff.endswith(passinfo):
    try:
        resp = channel.recv(9999)
    except Exception,e:
        print ('Error info:%s connection time.' % (str(e)))
        channel.close()
        ssh.close()
        sys.exit()
    buff += resp
    if not buff.find('yes/no')==-1:
        channel.send('yes\n')
    buff=''
 
channel.send(password+'\n')
 
buff=''
while not buff.endswith('# '):
    resp = channel.recv(9999)
    if not resp.find(passinfo)==-1:
        print 'Error info: Authentication failed.'
        channel.close()
        ssh.close()
        sys.exit()
    buff += resp
 
print (buff)
channel.close()
#TODO IMPORTANT TEMPLATE--------------
ssh.close()