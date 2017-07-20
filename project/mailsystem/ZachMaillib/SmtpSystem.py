# python day 22
# author zach.wang
# -*- coding:utf-8 -*-
import smtplib, sys, os, re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# TODO ONLY TEST NETEASE AND QQ mail
# options

receiver = ['wzq1397@live.cn', ]
subject = 'attachments'
smtpserver = 'smtp.qq.com'
port = 465
username = '641651925'
sender = username + '<641651925@qq.com>'
password = 'vatggmloaqchbbhi'

filepath = 'E:\\xml\\github\\'
picpath = 'E:\\xml\\github\\'

content = '''
            <html><h1>This is Zach.Wang</h1></html>
            <b>Some <i>HTML</i> text</b> and an image.<br><img src="cid:image1"><br>good!
        '''


def smtplib_login (msg):
    global port
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ';'.join(receiver)
    try:
        if 10 < port < 65535 :
            if port == 465 or port == 994:
                smtp = smtplib.SMTP_SSL()
            elif port == 25:
                smtp = smtplib.SMTP()
            else:
                choice = input("which type do you want to choose!\n1) NO_SSL\t2) SSL\n:>")
                if choice == '1' or choice == '\n':
                    smtp = smtplib.SMTP()
                elif choice == '2':
                    smtp = smtplib.SMTP_SSL()
                else:
                    sys.stderr.write("please choose right choice!\n")
        else:
            raise ValueError
    except Exception as e:
        print("INVAILD PORT!!!")
    smtp.connect(smtpserver, port)
    smtp.login(username, password)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()


class SmtplibSyntaxError(Exception):
    def __str__ (self):
        var = "WRONG SYNTAX!"
        return "%s" % var


def smtplib_text ():
    msg = MIMEText(content, 'html', 'utf-8')

    smtplib_login(msg)


def smtplib_attachement ():
    msg = MIMEMultipart('related')
    try:
        if filepath[-1] != '\\':
            att = MIMEText(open(filepath, 'rb').read(), 'base64', 'utf-8')
            att["Content-Type"] = 'application/octet-stream'
            # 使用re多文件中会出现无法识别编码问题！！！
            att["Content-Disposition"] = 'attachment; filename=' + str(re.compile(r'\\').split(filepath)[-1])
            msg.attach(att)
        else:
            for lst in os.listdir(filepath):
                att = MIMEText(open(filepath + lst, 'rb').read(), 'base64', 'utf-8')
                att["Content-Type"] = 'application/octet-stream'
                att.add_header("Content-Disposition", "attachment", filename=os.path.basename(lst))
                msg.attach(att)
    except (FileNotFoundError, AttributeError, PermissionError) as e:
        print(e)

    smtplib_login(msg)


def smtplib_pic ():
    msg = MIMEMultipart('related')

    msgText = MIMEText(content, 'html', 'utf-8')
    msg.attach(msgText)
    picdict = ['png', 'jpg', 'jpeg', 'gif']
    try:
        if picpath[-1] != '\\':
            if bool(picdict.index(re.compile(r'\.').split(os.path.basename(filepath))[-1])) == 0:
                fp = open(picpath, 'rb')
                msgImage = MIMEImage(fp.read())
                fp.close()
                msgImage.add_header('Content-ID', '<image-1>')
                msg.attach(msgImage)
            else:
                print("unsupport type!")
        else:
            for lst in os.listdir(picpath):
                tmp = re.compile(r'\.').split(os.path.basename(lst))[-1]
                if str(picdict).find(tmp) > -1:
                    fp = open(picpath + lst, 'rb')
                    msgImage = MIMEImage(fp.read())
                    fp.close()
                    info = os.path.basename(lst)
                    msgImage.add_header('Content-ID', "<%s>" % info)
                    msg.attach(msgImage)
                else:
                    pass
    except (FileNotFoundError, AttributeError, PermissionError, ValueError) as e:
        print(e)

    smtplib_login(msg)


global flag
flag = 0
try:
    if len(sys.argv) <= 2:
        if str(sys.argv[1]).lower() == "text":
            smtplib_text()
            flag = 1
        if str(sys.argv[1]).lower() == "attachement" or str(sys.argv[1]).lower() == "attach":
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
