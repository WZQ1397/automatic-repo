# python day 21
# author zach.wang
# -*- coding:utf-8 -*-
import random

def get_userName(user_length):
    if user_length > 62:
        user_length = 62
    __userName = ''.join(random.sample("1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",user_length))
    return __userName

def get_Password(passwd_length):
    if passwd_length > 62:
        passwd_length = 62
    __userPassword = ''.join(random.sample("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_.1234567890",passwd_length))
    return __userPassword
try:
    pass
    #print("用户名:", get_userName(8))
    #print("密码:", get_Password(8))
except Exception as e:
    print(e)