#!/usr/bin/env python
# codind:utf-8

import os
import time
import threading
import pycurl
import urllib2

def Master_Status():
	return os.system("sh Master_Status.sh")

def Slave_Status():
	return os.system("sh Slave_Status.sh")

def Io_Status():
	return os.system("sh Io_Status.sh")

def Main():
	Io = Io_Status()
	
	t1 = threading.Thread(target=Master_Status)
	t2 = threading.Thread(target=Slave_Status)

	MasterPosNum = t1.start()
	SlavePosNum = t2.start()
	
	if MasterPosNum != SlavePosNum or Io != 0:
		urllib2.urlopen('http://www.baidu.com').read()

if __name__ == '__main__':
		Main()
