import smtplib
from email.mime.text import MIMEText
from email.header import Header
def sedmail():
    sender = 'wzq1397@live.cn'
    receivers = ['641651925@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    message = MIMEText('Python 邮件发送测试...内容', 'plain', 'utf-8')
    message['From'] = Header("wzq1397", 'utf-8')
    message['To'] =  Header("641651925", 'utf-8')

    subject = 'Python SMTP 标题'
    message['Subject'] = Header(subject, 'utf-8')


    try:
        smtpObj = smtplib.SMTP('localhost')
        smtpObj.sendmail(sender, receivers, message.as_string())
        print ("邮件发送成功")
    except smtplib.SMTPException:
        print ("Error: 无法发送邮件")

#for i in range(10):
    sedmail()
