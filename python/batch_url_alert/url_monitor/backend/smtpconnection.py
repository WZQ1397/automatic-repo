#!/usr/bin/python
# -*- encoding: utf-8 -*-


import logging
import smtplib
from email.mime.text import MIMEText

from pony_monitor.conf import settings


class SMTPConnection(object):
    """
        以后支持HTML的邮件
    """

    def __init__(self, host=None, port=None, username=None, password=None,
                 use_tls=None, fail_silently=False):
        self.host = host or settings.EMAIL_HOST
        self.port = port or settings.EMAIL_PORT
        self.username = username or settings.EMAIL_HOST_USER
        self.password = password or settings.EMAIL_HOST_PASSWORD
        self.use_tls = (use_tls is not None) and use_tls or settings.EMAIL_USE_TLS
        self.fail_silently = fail_silently
        self.connection = None

    def open(self):
        """
        Ensures we have a connection to the email server. Returns whether or
        not a new connection was required (True or False).
        """
        if self.connection:
            # Nothing to do if the connection is already open.
            return False
        try:
            self.connection = smtplib.SMTP(self.host, self.port)
            if self.use_tls:
                self.connection.ehlo()
                self.connection.starttls()
                self.connection.ehlo()
            if self.username and self.password:
                self.connection.login(self.username, self.password)
            return True
        except:
            if not self.fail_silently:
                raise

    def close(self):
        """Closes the connection to the email server."""
        try:
            try:
                self.connection.quit()
            except socket.sslerror:
                # This happens when calling quit() on a TLS connection
                # sometimes.
                self.connection.close()
            except:
                if self.fail_silently:
                    return
                raise
        finally:
            self.connection = None

    def send(self, recipients, from_email, subject, message):
        """A helper method that does the actual sending."""

        # Create a text/plain message
        msg = MIMEText(message)

        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = ','.join(recipients)

        try:
            self.connection.sendmail(from_email, recipients, msg.as_string())
        except Exception, e:
            logging.error(e)
            if not self.fail_silently:
                raise
            return False
        return True
