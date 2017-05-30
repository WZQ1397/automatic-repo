#! /bin/bash

# Zabbix Email alter shell script
# msmtp is an SMTP client

#vi /usr/local/msmtp/etc/msmtprc #手动创建配置文件 
#account default 
#host smtp.163.com #你的发送邮件服务器 
#port 25 
#from xman@163.com #要从哪个邮箱发出 
#auth login #这里如果使用on的话会报 "msmtp: cannot use a secure authentication method"错误 
#tls off 
#user xman@163.com #邮箱用户名 
#password xmanufo  #邮箱密码，这里可是明文的，如果你觉得不安全可以把文件改为600属性 
#logfile /var/log/mmlog 
DEBUG=1
if [[ ${DEBUG} -gt 0 ]];then
    exec 2>>/tmp/zabbix_msmtp.log
    set -x
fi
FROM='example@example.com'
account_name='zabbix'
# Parameters (as passed by Zabbix):
#  $1 : Recipient
#  $2 : Subject
#  $3 : Message
recipient=$1
subject=$2
message=$3
date=`date --rfc-2822`
sed 's/$/\r/' <<eof | /usr/bin/msmtp --account ${account_name} ${recipient}
From: <${FROM}>
To: <${recipient}>
Subject: ${subject}
Date: ${date}
${message}
eof