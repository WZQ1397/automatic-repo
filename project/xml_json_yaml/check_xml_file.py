#!/usr/bin/python
import xml.parsers.expat,sys
from glob import glob

#TODO check xml file syntax
COLOR_NONE = "\033[m"
COLOR_GREEN = "\033[01;32m"
COLOR_RED = "\033[01;31m"
COLOR_YELLOW = "\033[01;33m"

def parsefile(file):
    parser = xml.parsers.expat.ParserCreate()
    parser.ParseFile(open(file, "rb"))

for arg in ['E:\python\movies.xml']:
    for filename in glob(arg):
        try:
            parsefile(filename)
            print(COLOR_GREEN+"%s is well-formed" % filename)
        except Exception as e:
            print(COLOR_RED+"%s is %s" % (filename, e))
