# -*- coding: utf-8 -*-
# Author: Zach.Wang
# @Time  : 2020-02-02 20:52
# asyncio 没有提供http协议的接口
import asyncio
import time
from urllib.parse import urlparse


async def get_url(url):
    url = urlparse(url)
    host,path = url.netloc, '/' if url.path == '' else url.path

    # 建立连接
    # asyncio.open_connection是一个协程
    reader, writer = await asyncio.open_connection(host, 80)
    writer.write("GET {} HTTP/1.1\r\nHost:{}\r\nConnection:close\r\n\r\n".format(path, host).encode('utf-8'))
    all_lines = [ raw_line.decode('utf-8') async for raw_line in reader ]

    return '\n'.join(all_lines)


async def main(start=1,end=10):
    tasks = []
    for url in range(start,end):
        url = 'http://shop.projectsedu.com/goods/{}/'.format(url)
        tasks.append(asyncio.ensure_future(get_url(url)))
    for task in asyncio.as_completed(tasks):
        # asyncio.as_completed返回的是一个协程
        result = await task
        print(result)


if __name__ == '__main__':
    start_time = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(1,2))
    print('last time:{}'.format(time.time() - start_time))