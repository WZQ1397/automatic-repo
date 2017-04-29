#!/usr/bin/python
# -*- encoding: utf-8 -*-

import logging

class ConsoleAlert(object):

    def alert(self, url, expected_code, code):
        if code:
            logging.error("ALERT %s returned %d, expected %d" % (url, expected_code, code))
        else:
            logging.error("ALERT failed to connect to %s" % url)

    def back_to_normal(self, url, code):
        logging.info("Back to normal %s" % url)
