#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-

def confirm(question, default=True):
    """
    Ask user a yes/no question and return their response as True or False.
    :parameter question:
    By default, when the user presses Enter without typing anything, "yes" is
    assumed. This can be changed by specifying ``default=False``.
    :return True or False
    """
    # Set up suffix
    if default:
        suffix = "Y/n"
    else:
        suffix = "y/N"
    # Loop till we get something we like
    while True:
        response = raw_input("%s [%s] " % (question, suffix)).lower()
        # Default
        if not response:
            return default
        # Yes
        if response in ['y', 'yes']:
            return True
        # No
        if response in ['n', 'no']:
            return False
        # Didn't get empty, yes or no, so complain and loop
        print("I didn't understand you. Please specify '(y)es' or '(n)o'.")