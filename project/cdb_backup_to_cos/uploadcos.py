#!/bin/env python
# -*- coding:utf-8 -*-
# _auth:kaliarch
# use cos-python-sdk-v5
# https://cloud.tencent.com/document/product/436/12269

import os
import configparser
import requests
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client


class CosOper():
    def __init__(self):
        """
        读取配置文件，初始化变量
        """
        config = configparser.ConfigParser()
        config.read('config.txt')
        self.secret_id = config['common']['secret_id']
        self.secret_key = config['common']['secret_key']
        self.cos_region = config['cosinfo']['cos_region']
        self.bucket_name = config['cosinfo']['bucket_name']

    def get_cos_client(self):
        """
        实例化cos clinet
        :return: cos client
        """
        config = CosConfig(Secret_id=self.secret_id, Secret_key=self.secret_key, Region=self.cos_region)
        cos_client = CosS3Client(config)
        return cos_client

    def cos_upload(self, filename, url, cos_client):
        """
        简单文件上传
        :param filename: object name
        :param url: 网络url
        :param cos_client:
        :return:
        """
        response = cos_client.put_object(
            Bucket=self.bucket_name,
            Body=requests.get(url).content,
            Key=filename
        )
        return response

    def cos_upload_file(self, filename, url, cos_client, partsize=10, maxthread=5):
        """
        根据文件大小自动选择简单上传或分块上传，分块上传具备断点续传功能。
        :param filename:
        :param cos_client:
        :param partsize:
        :param maxthread:
        :return:
        """
        # 下载到本地文件
        with open(filename, 'wb') as localfile:
            localfile.write(requests.request('get', url).content)
        # 进行上传
        response = cos_client.upload_file(
            Bucket=self.bucket_name,
            LocalFilePath=filename,
            Key=filename,
            PartSize=partsize,
            MAXThread=maxthread
        )
        # 删除本地文件
        if os.path.exists(filename):
            os.remove(filename)
        return response['ETag']


if __name__ == '__main__':
    test_filename = 'test_file_name'
    test_url = 'https://sh-dl-cdb.qcloud.com/5ff2a7d11dd677d13f50bb036c52645e?appid=1253961596&time=1531707978&sign=KFWgPCIdW8t%2Fx%2Bj04qgQ8sU2dlA%3D'
    cosoper = CosOper()
    client = cosoper.get_cos_client()
    # 普通上传
    # client.upload_file()
    # 高级上传
    result = cosoper.cos_upload_file(test_filename, test_url, client)
    print(result)
