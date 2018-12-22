#!/bin/env python
# -*- coding:utf-8 -*-
# _auth:kaliarch

import getcdbbakurl
import uploadcos
import loghelper


def log_helper():
    """
    实例化loger,创建logdir及返回logger
    :return: logger对象
    """
    LogHeper = loghelper.LogHelper()
    logfile_name = LogHeper.create_dir()
    logger = LogHeper.create_logger(logfile_name)
    return logger


def cdbhelper(logger):
    """
    实例化cdb操作，通过cdb的api获取备份文件名称和下载url
    :return: cdb备份文件名称和下载url
    """
    CdbOper = getcdbbakurl.CdbOper()
    # 获取请求参数dict
    keydict = CdbOper.get_dict()
    logger.info('get keydict success')
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
    logger.info("cdb-bakname: %s,download_url: %s,download_size:%sM" % (cdbbak_name, download_url,download_size))
    return cdbbak_name, download_url


def coshelper(bak_name, download_url, logger):
    """
    实例化cos，完成备份文件上传
    :param bak_name:
    :param download_url:
    :return:
    """
    CosOper = uploadcos.CosOper()
    cos_client = CosOper.get_cos_client()
    logger.info('get cos client success!')
    # 简单文件上传
    # cos_response = CosOper.cos_upload(filename=bak_name,url=download_url,cos_client=cos_client)

    # 高级上传
    cos_response = CosOper.cos_upload_file(filename=bak_name, url=download_url, cos_client=cos_client)


def run():
    logger = log_helper()
    cdbbak_name, download_url = cdbhelper(logger)
    coshelper(cdbbak_name, download_url, logger)


if __name__ == '__main__':
    run()
