#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import sys
import os
from url_monitor.runner import main

sys.path.append(os.getcwd())

os.environ['SETTINS_MODULE'] = 'settings'

if __name__ == '__main__':
    main()
