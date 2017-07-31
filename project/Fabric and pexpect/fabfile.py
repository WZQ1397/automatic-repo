from fabric.api import *
from fabric.context_managers import *
from fabric.colors import *
import sys

env.roledefs={'mongo':['172.16.6.202','172.16.6.203']}
env.user='root'
env.password='edong'

@roles('mongo')
def remoteexec1():
    with cd('/var/log/'):
        run('ls')
    open_shell("ifconfig")

#TODO ONLY RUN FIRST
@runs_once
def localexec():
    print(red('IPV4 INFO'))
    print(local('echo ZACH'))
    #FIXME NOT IDEAL
    '''
    f = open('sysinfo.bin','w')
    sys.stdout=f
    local('ipconfig | findstr IPv4')
    '''

def deploy():
    execute(remoteexec1)
    execute(localexec)
    execute(localexec)