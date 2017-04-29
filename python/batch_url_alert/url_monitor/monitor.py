#!/usr/bin/python
# -*- encoding: utf-8 -*-

import logging
import datetime
import time
from urllib2 import urlopen, URLError, HTTPError
from import_utils import get_instance

class Monitor(object):
    """ monitor url """

    def __init__(self, backends, timeout):
        self.failed = set()
        self.timeout = timeout
        self.alert_backend = []
        self.create_alert_backends(backends)

    def create_alert_backends(self, backends):
        print backends
        for b in backends:
            ins = get_instance(b)
            if ins:
                self.alert_backend.append(ins)

    def set_url_as_failed(self, url, code):
        """ mark url as failed """
        self.failed.add((url, code))

    def is_failed(self, url, code):
        return (url, code) in self.failed

    def return_to_normal(self, url, code):
        self.failed.remove((url, code))
        for b in self.alert_backend:
            b.back_to_normal(url, code)

    def check_url(self, url):
        """ check for an url. return code
        """
        try:
            ret_code = urlopen(url, timeout=self.timeout).getcode() 
            logging.debug("returned %d" % ret_code)
            return ret_code
        except HTTPError, e:
            return e.getcode()
        except URLError,e:
            pass
        return None

    def send_alert(self, url, expected_code, code):
        logging.info("check %s FAILED!" % url)
        logging.info("sending alert")
        for b in self.alert_backend:
            b.alert(url, expected_code, code)

    def check(self, urls_to_check,callBackUri):
        for url, expected_code in urls_to_check:
            logging.debug("checking %s whit code %d" % (url, expected_code))
            code = self.check_url(url)
            if not code or code != expected_code:
                if not self.is_failed(url, expected_code):
                    self.send_alert(url, expected_code, code)
                self.set_url_as_failed(url, expected_code)
            else:
                if self.is_failed(url, expected_code):
                    self.return_to_normal(url, expected_code)


