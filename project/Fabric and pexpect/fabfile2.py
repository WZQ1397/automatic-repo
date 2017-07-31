from fabric.api import *
from fabric.colors import *
from fabric.context_managers import *

#TODO SET DIFF ROLE
env.roledefs = {
    'mongodb': ['172.16.6.202','172.16.6.203'],
    'build': ['172.16.10.120']
}

env.user='root'
env.password='edong'
'''
env.passwords = {
    'mongodb': 'edong',
    'build': 'edong'
}
'''
@roles('mongodb')
def task1():
    run('df -h')

@roles('build')
def task2():
    print(green("I'm fabric"))
    with hide('running', 'stdout', 'stderr'):
        sudo('free')
    name = run('hostname')
    #TODO content manage
    with cd('/var/log/'):
        with lcd('/'):
            #TODO get <--> put(local, remote)
            get('mongodb.log',name+'.log')

#@parallel(pool_size=10)
def deploy():
    execute(task1)
    execute(task2)
    with settings(abort_on_prompts=False):
        opt = prompt('do you want to exec again?\n',default='No',validate=str)
    if opt.lower() == 'y' or opt.lower() == 'yes':
        deploy()
    else:
        pass
        #TODO REBOOT MACHINE!!!
        #reboot(wait=60)