#!/usr/bin/python
# -*- encoding: utf-8 -*-


import logging

from smtpconnection import SMTPConnection

from pony_monitor.conf import settings

logger = logging.getLogger('MAILBACKEND')

class MailAlert(object):

    def send_mail(self, subject, msg):
        s = SMTPConnection()
        try:
            s.open()
        except Exception, e:
            logging.error(e)
            logging.error("can't open connection")
        pre_subject = getattr(settings, "SUBJECT_PREFIX", 'alert from xiaorui.cc')
        s.send(settings.RECIPIENTS, settings.EMAIL_HOST_USER, pre_subject + subject, msg)
        s.close()

    def alert(self, url, expected_code, code):
            
        if code:
            msg = "ALERT %s returned %d, expected %d" % (url, code, expected_code)
        else:
            msg = "ALERT failed to connect to %s" % url
        self.send_mail("ALERT", msg)

    def back_to_normal(self, url, code):
        logging.info("Back to normal %s" % url)
        self.send_mail("back to normal", "%s has turned stable" % url)
