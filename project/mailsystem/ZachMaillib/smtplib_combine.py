# python day 22
# author zach.wang
# -*- coding:utf-8 -*-
import smtplib,sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

#options
sender = '641651925@qq.com'
receiver = 'wzq1397@live.cn'
subject = 'python email test'
smtpserver = 'smtp.qq.com'
port = '465'
username = '641651925'
password = 'vatggmloaqchbbhi'
filepath = 'E:\\python\\redis.png'
picpath = 'E:\\python\\redis.png'

def smtplib_login(msg):
    smtp = smtplib.SMTP_SSL(smtpserver,port)
    smtp.login(username, password)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()

class SmtplibSyntaxError(Exception):

    def __str__(self):
        var = "WRONG SYNTAX!"
        return "%s" %var

def smtplib_text():
    msg = MIMEText('<html><h1>This is Zach.Wang</h1></html>','html','utf-8')
    msg['Subject'] = subject

    smtplib_login(msg)

def smtplib_attachement():
    msg = MIMEMultipart('related')

    #构造附件
    att = MIMEText(open(filepath, 'rb').read(), 'base64', 'utf-8')
    att["Content-Type"] = 'application/octet-stream'
    att["Content-Disposition"] = 'attachment; filename="redis bit"'
    msg.attach(att)

    smtplib_login(msg)

def smtplib_attachement():
    msg = MIMEMultipart('related')

    #构造附件
    att = MIMEText(open(filepath, 'rb').read(), 'base64', 'utf-8')
    att["Content-Type"] = 'application/octet-stream'
    att["Content-Disposition"] = 'attachment; filename="redis bit"'
    msg.attach(att)

    smtplib_login(msg)

def smtplib_pic():
    msg = MIMEMultipart('related')
    msg['Subject'] = 'test message'

    msgText = MIMEText('<b>Some <i>HTML</i> text</b> and an image.<br><img src="cid:image1"><br>good!','html','utf-8')
    msg.attach(msgText)
    
    fp = open(picpath, 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()

    msgImage.add_header('Content-ID', '<image1>')
    msg.attach(msgImage)

    smtplib_login(msg)

global flag
flag = 0
try:
    if len(sys.argv)>2:
        if str(sys.argv[1]).lower() == "text":
            smtplib_text()
            flag = 1
        if str(sys.argv[1]).lower() == "attachement" or str(sys.argv[1]).lower() == "attach" :
            smtplib_attachement()
            flag = 1
            print(len(sys.argv))
        if str(sys.argv[1]).lower() == "pic":
            smtplib_pic()
            flag = 1
        if flag != 1:
            raise SmtplibSyntaxError()
    else:
        raise SmtplibSyntaxError()
except SmtplibSyntaxError as e:
    print(e)
finally:
    if flag == 1:
        print("send sucessfull!")
    else:
        print("send failed!")

