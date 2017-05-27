#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-

# https://pypi.python.org/pypi/progress/1.2
# pip used
from progress.bar import Bar
import time

bar = Bar('Processing', max=20)
for i in range(20):
    # Do some work
    time.sleep(1)
    bar.next()
bar.finish()