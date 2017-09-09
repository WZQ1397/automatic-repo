#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-

import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.6.28.36", port=20122, username="root", key_filename="id_rsa")
stdin, stdout, stderr = client.exec_command("uname -a")
for line in stdout:
    print line,
client.close()