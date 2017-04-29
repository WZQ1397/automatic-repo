#!/usr/bin/python
# -*- encoding: utf-8 -*-

import os
import logging
import importlib



try:
    SETTINGS_MODULE = os.environ['SETTINS_MODULE']
except:
    raise Exception, "you need to have settings.py file"


#SETTINGS_MODULE= 'settings'

try:
    settings = importlib.import_module(SETTINGS_MODULE)
except ImportError, e:
    raise ImportError, "Could not import settings  %s" % (SETTINGS_MODULE)






