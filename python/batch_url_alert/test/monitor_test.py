#!/usr/bin/python
# -*- encoding: utf-8 -*-

from url_monitor.monitor import Monitor


class MonitorTest(Monitor):

    def __init__(self, code, *args, **kwargs):
        self.code = code 
        super(MonitorTest, self).__init__(*args, **kwargs)

    def check_url(self, url):
        return self.code


urls_to_check = (('url1', 200), ('url2',500))

def test_check():
    m = MonitorTest(500, [], 20)
    m.check(urls_to_check)
    assert urls_to_check[0] in m.failed
    assert urls_to_check[1] not in m.failed


def test_back_to_normal():
    m = MonitorTest(500, [], 20)
    m.check(urls_to_check)
    assert urls_to_check[0] in m.failed
    m.code = 200
    m.check(urls_to_check)
    assert urls_to_check[0] not in m.failed

