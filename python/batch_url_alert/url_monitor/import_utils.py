#!/usr/bin/python
# -*- encoding: utf-8 -*-

import logging
from importlib import import_module


def get_instance(class_name, **kwargs):
    """ load an instance given class name """
    try:
        dot = class_name.rindex('.')
    except ValueError:
        logging.error("can't parse class name: %s", class_name)
        return None

    module, classname = class_name[:dot], class_name[dot+1:]
    try:
        mod = import_module(module)
    except ImportError, e:
        logging.error(e)
        logging.error("can't load module: %s", module)
        return None
    try:
        mw_class = getattr(mod, classname)
    except AttributeError:
        logging.error("can't get class: %s", classname)

    return mw_class(**kwargs)


