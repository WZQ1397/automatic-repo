#!/usr/bin/env python
import paramiko
import os,sys,time
 
hostname="192.168.1.111"   # Զ������
username="root"                    # Զ���������û���
password="SKJh935yft#"
 
blip="192.168.1.1"              # ���ݻ�
bluser="root"                        #���ݻ��û���
blpasswd="SKJh935yft#"
 
tmpdir="/tmp"                   #  �ͻ���Դ�ļ�·�������ݻ���ʱ·����Զ������Ŀ���ļ�·��
remotedir="/data"             
localpath="/home/nginx_access.tar.gz"
tmppath=tmpdir+"/nginx_access.tar.gz"
remotepath=remotedir+"/nginx_access_hd.tar.gz"
 
port=22
passinfo='\'s password: '                     # ����������Ϣ
paramiko.util.log_to_file('syslogin.log')   # paramiko�Դ�����־����
 
t = paramiko.Transport((blip, port))           # �������Ӷ���
t.connect(username=bluser, password=blpasswd)   #��������
sftp =paramiko.SFTPClient.from_transport(t)  # ����SFTP����
sftp.put(localpath, tmppath)    # ����put�����ϴ��ļ�
 
sftp.close()          # �ر�sftp����
 
ssh=paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname=blip,username=bluser,password=blpasswd)

#TODO IMPORTANT TEMPLATE--------------
#����һ���µĻỰ
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