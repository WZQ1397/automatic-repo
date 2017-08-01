import pexpect
import getpass
import time


try:
    raw_input
except NameError:
    raw_input = input


# SMTP:25 IMAP4:143 POP3:110
tunnel_command = 'ssh -C -N -f -L 25:127.0.0.1:25 -L 143:127.0.0.1:143 -L 110:127.0.0.1:110 %(user)@%(host)'
host = raw_input('Hostname: ')
user = raw_input('Username: ')
X = getpass.getpass('Password: ')

def get_process_info ():
    ps = pexpect.run ('ps ax -O ppid')
    pass

def start_tunnel ():

    try:
        ssh_tunnel = pexpect.spawn (tunnel_command % globals())
        ssh_tunnel.expect ('password:')
        time.sleep (0.1)
        ssh_tunnel.sendline (X)
        time.sleep (60) # Cygwin is slow to update process status.
        ssh_tunnel.expect (pexpect.EOF)

    except Exception as e:
        print(str(e))

def main ():
    while True:
        ps = pexpect.spawn ('ps')
        time.sleep (1)
        index = ps.expect (['/usr/bin/ssh', pexpect.EOF, pexpect.TIMEOUT])
        if index == 2:
            print('TIMEOUT in ps command...')
            print(str(ps))
            time.sleep (13)
        if index == 1:
            print(time.asctime(), end=' ')
            print('restarting tunnel')
            start_tunnel ()
            time.sleep (11)
            print('tunnel OK')
        else:
            # print 'tunnel OK'
            time.sleep (7)

if __name__ == '__main__':
    main ()