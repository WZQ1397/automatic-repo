import pexpect,subprocess
from pexpect import run
from pexpect.pxssh import pxssh
# TODO NOT SUPPORT WIN!!!
ip="172.16.10.120"
name="root"
pwd="edong"

child = pexpect.spawn('ssh  '+name+'@%s' %ip )

#TODO LOG HISTROY
log = open('/var/log/pexpect.log','w')
child.logfile = log

#TODO NOTICE FINGERPRINT
chk = child.expect(['yes',pexpect.TIMEOUT],timeout=10)

def first_run():
    #TODO send is not next line
    child.sendline('yes')

def exec1():
    child.expect ('password:')
    child.sendline(pwd)
    child.expect('#')
    child.sendline('df -h')

def exec2():
    child.expect('#')
    if subprocess.getstatusoutput('id root >> /dev/null 2&1  && echo $?') != 0:
        __newpasswd = 'edong&1310'
        subprocess.getstatusoutput('useradd zach')
        run('passwd zach',events={'(?i)password:':__newpasswd})
        #TODO run EQUAL TO FOLLOW COMMIT!
        '''
        child.expect('password:')
        child.sendline()
        child.expect('password:')
        child.sendline(__newpasswd)
        '''
        child.expect('#')
        child.sendline('su - zach')
    child.expect('$')
    child.sendline('whomai')

if chk == 1:
    first_run()
    exec1()
elif chk == 0:
    exec1()
else:
    # TODO EQUAL TO <CTRL+C>
    child.sendcontrol('c')