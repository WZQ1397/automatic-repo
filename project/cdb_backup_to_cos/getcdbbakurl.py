#!/bin/env python
# -*- coding:utf-8 -*-
# _auth:kaliarch
# use cdb api

import configparser
import time
import random
import hmac
import hashlib
import base64
import requests
import json
from urllib import parse


class CdbOper():
    def __init__(self):
        """
        读取配置文件，初始化变量
        """
        config = configparser.ConfigParser()
        config.read('config.txt')
        self.secret_id = config['common']['secret_id']
        self.secret_key = config['common']['secret_key']
        self.cdb_region = config['cdbinfo']['cdb_region']
        self.cdb_instanceid = config['cdbinfo']['cdb_instanceid']
        self.cdb_bak_type = config['cdbinfo']['cdb_bak_type']
        self.cdb_api_url = 'cdb.api.qcloud.com/v2/index.php?'
        self.cdb_action = 'GetCdbExportLogUrl'

    def get_dict(self):
        """
        生成公共参数字典
        :return: 公共参数字典
        """
        keydict = {
            'Action': self.cdb_action,
            'Timestamp': str(int(time.time())),
            'Nonce': str(int(random.random() * 1000)),
            'Region': self.cdb_region,
            'SecretId': self.secret_id,
            # 'SignatureMethod': SignatureMethod,
            'cdbInstanceId': self.cdb_instanceid,
            'type': self.cdb_bak_type
        }
        return keydict

    def sort_dic(self, keydict):
        """
        对字典进行排序
        :param keydict:
        :return: 返回排序后的列表
        """
        sortlist = sorted(zip(keydict.keys(), keydict.values()))
        return sortlist

    def get_str_sign(self, sortlist):
        """
        将排序后的列表进行字符串拼接
        :param sortlist:
        :return: 拼接后的字符串
        """
        sign_str_init = ''
        for value in sortlist:
            sign_str_init += value[0] + '=' + value[1] + '&'
        sign_str = 'GET' + self.cdb_api_url + sign_str_init[:-1]
        return sign_str, sign_str_init

    def get_signature(self, sign_str):
        """
        生成签名
        :param sign_str:
        :param secretkey:
        :return:签名字符串
        """
        secretkey = self.secret_key
        signature = bytes(sign_str, encoding='utf-8')
        secretkey = bytes(secretkey, encoding='utf-8')
        my_sign = hmac.new(secretkey, signature, hashlib.sha1).digest()
        my_sign = base64.b64encode(my_sign)
        return my_sign

    def encode_signature(self, my_sign):
        """
        对签名编码
        :param my_sign:
        :return: 编码后的签名串
        """
        result_sign = parse.quote(my_sign)
        return result_sign

    def get_result_url(self, sign_str, result_sign):
        """
        完成最终url拼接
        :param result_sign:
        :return: 最终url
        """
        result_url = 'https://' + self.cdb_api_url + sign_str + '&Signature=' + result_sign
        return result_url

    def get_response(self, result_url):
        """
        发送get请求
        :param result_url:
        :return: 返回相应信息
        """
        response = requests.request('get', result_url)
        if response.status_code == 200:
            return response
        else:
            print('occer error')

    def get_cdbbak_url(self, response):
        """
        获取cdb的文件名和cdb下载链接
        :param response:
        :return:cdb filename downloadurl
        """
        result_data = json.loads(response.text)
        data = result_data['data'][-1]
        download_filename = parse.unquote_plus(data['file_name'])
        download_url = data['out_url']
        download_size = int(data['size'] / 1024 / 1024)
        return download_filename, download_url ,download_size


if __name__ == '__main__':
    CdbOper = CdbOper()
    # 获取请求参数dict
    keydict = CdbOper.get_dict()
    # 对参数dict进行排序
    sortlist = CdbOper.sort_dic(keydict)
    # 获取拼接后的sign字符串
    sign_str, sign_str_int = CdbOper.get_str_sign(sortlist)
    # 获取签名
    my_sign = CdbOper.get_signature(sign_str)
    # 对签名串进行编码
    result_sign = CdbOper.encode_signature(my_sign)
    # 获取最终请求url
    result_url = CdbOper.get_result_url(sign_str_int, result_sign)
    # 调用api
    cdb_response = CdbOper.get_response(result_url)
    # 获取cdb 备份名称和下载链接
    cdbbak_name, download_url ,download_size= CdbOper.get_cdbbak_url(cdb_response)
    print('cdbbak_name: %s, \ncdb_download_url:,%s,\ncdb_download_size:,%sM' % (cdbbak_name, download_url,download_size))
