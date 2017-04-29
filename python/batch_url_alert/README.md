## 支持批量自定义的URL探测报警及URL回调

1. vim setting.py

```
URLS_TO_CHECK = (
        ('http://localhost:8080/', 200),
        )


# 超时
TIMEOUT = 5

# 间隔时间
CHECK_INTERVAL = 3

#报警的相关模块
ALERT_BACKENDS = ('url_monitor.backend.mail.MailAlert',)

#回调的URl
ALERT_CALLBACK = ('http://127.0.0.1/url/error_api')

#show web ui ip:port
WEBUI = '127.0.0.1:8888'

# 你的邮箱
EMAIL_HOST = 'smtp.163.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'xiaorui@163.com'
DEFAULT_FROM_EMAIL=EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = True

# 收到的告警邮箱
RECIPIENTS = ['rfyiamcool@163.com']

```

2. python Urlmonitor.py
3. open mailindex to check alert mail

-------
TODO:

websocket实时页面
自定义其他的类型的探测

