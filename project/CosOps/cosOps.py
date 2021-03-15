# -*- coding=utf-8
from qcloud_cos import CosConfig, CosS3Client, CosServiceError
from config import *
import sys
import logging


class TencentOSS:
    _client: CosS3Client
    newbkList: list

    def __init__(self, secret_id, secret_key, region, token=None, scheme='https'):
        logging.basicConfig(level=logging.WARNING, stream=sys.stdout)
        config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
        self._client = CosS3Client(config)
        self.newbkList = []
        self.APPID = APPID

    def createBuckets(self, bkList):
        # create bucket
        for bk in bkList:
            response = self._client.create_bucket(
                Bucket=f"{bk}-{self.APPID}"
            )
            self.newbkList.append(f"{bk}-{self.APPID}")

    @property
    def getBuckets(self):
        return self._client.list_buckets()['Buckets']['Bucket']

    def checkBucketsExists(self,bucket):
        try:
            self._client.head_bucket(
                Bucket=bucket
            )
        except CosServiceError as _:
            return False
        return True

