# python day 13
# author zach.wang
# -*- coding:utf-8 -*-
import paramiko
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

priv_str = """-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEAvWpKpr7DGDNCA+qVNrixqlX0NvPIXFMS2K5CMgo1M+iHKrjv
2aPK6m9xmiMe6XUnX70o1xP9Y4/vpJzXHaEx9iUzUWJUbFeNC0qTvjVKoQYUMsJG
WjwjqpNzunoALNnoBc221ZOM4d4OwkHIAsMNhEJwXC/tl1MnJDHDYwOAfeIn7jTc
8kBmsRkazSUxUUIkrI/npv3a7E6g4hWTiRshWHhTl9yn0BZdghjajTLR1dUKeCH9
CJ+ChVOYTcRRYuqUGBS18x0I8S8Py5kLhkQGQF+wRgxVRjEX3GyoZRJ8zk4ptjru
Wq2hsv48R1XFMj2PhGtuyF2vqgh8pocNGbAbYwIBIwKCAQEAnPGrkXl9FA02ssmu
1ZG3x6ZOAaVrf7KL9V0viIwddCcQ6OJgVT6SL/XwacVUIIWkSAMh1sdrjQI7lwWc
S8ATdC1zqdUhYRVXm6QxRdRiaCmbtQde3Q1CH56++ZhJSbvdgSbKsPaZTW7ZB1sT
cACzbZYilYbMLO0gbnJgEDYaAeXVctOQD1JMduNn1C6lfljZ3dsAKmRqXAJrEDOt
4/F7Bl/UGfmZQRzW6XJVRnFLyGbwpk1XVoAnClFwD9tbg5ibB0Hem687KcVVzxof
+/TrLX2/DmfRKNArxQdybbVNzqjfEZMBxqYf1zJpySh+gpo4tGWHClHob1rGSF2D
xxMFWwKBgQD73JgSTUspMkTbj2tX0SCtU8NzzRWBGgEjKj8j2o5VyDsJSy2T+bes
ovtP48VG8cRD6oFoOpvylp4YBRWD6scd2rCxswiVE32QRplEpgnD9ShMQhK6qBTr
RNEAdek8zUyq7QjJyrVdHQx3pWj6YQ3CUU9zIgadETchR+/F8YPhOwKBgQDAhwdj
ZlQfAP+VyuKn1fzaVd6fyg4ObBWbZn2U/Iyp1/6Zw2da4A+/JnkSFp4vbcmAzb7T
Hv724kGPGw/96viGK83l7h2oDGI7RG189sM4HSQKq/fkzfTLoPyZasExjAC4L5Jg
NkpBd73Ai9ZnGRSRly6w8ikvCZjEVrOoHW2L+QKBgEDDshNVtD3LGQVCIuqyHlh0
n/k0vGMGr9XXqdYFAAduAI1ceW8xlaFrvPdJMrp4rs+is4/UjoA1W9pKcz8tviw/
jIV3Lhe0jgCHLrnhjXuILu8JrQttDLGGuWaEuFF2nq+cCZL5nFnFpB7EIk8DA4m9
Iw76HvUwUAE+Yjo2yiP5AoGBAIQE0d3CgtNuZh2Sb4kHw1PjHFBQCaN9UKUTFEjn
sOl+Ku0YRt86jnRyJyJYpvvzgtv6y/57p4S4Z3gSjp98jSjNlIBow+DyjIBpb6Yl
jS3K1uK/EGJhV2cPTiAOsFx9QlJpw3UsirCMn1911Nj7QU3kAsJ6Kt5s+wpKFMsM
3WdLAoGAGBPkHq3TUXEVrQQbGDMsi1b6vBB9sW1xU6uzXVX1zWNxye+7ETazl4+8
YFtBG5fRs86uvQd1gfYZCYkBk+pCh8nsMswuhh5jIEgvnxCKF9OEQugjp/gjAYqc
U81RlNbwezBrqj89Hffq7slsEmc3RECi8TyelimOJck2KD9Kg7g=
-----END RSA PRIVATE KEY-----"""

hostname = "172.16.6.226"
port = 22
username = 'root'
passwd = 'edong'
cmd = 'uptime'

priv_key = paramiko.RSAKey(file_obj=StringIO(priv_str))
paramiko.util.log_to_file('paramiko.info')
trans_mode = paramiko.Transport((hostname,port))
trans_mode.connect(username=username,password=passwd,pkey=priv_key)
ssh = paramiko.SSHClient()
ssh._transport = trans_mode
stdin , stdout, stderr = ssh.exec_command(cmd)

res = stdout.read()
print(res.decode())
trans_mode.close()
