from __future__ import unicode_literals
import pexpect
import sys

child = pexpect.spawnu('ftp ftp.openbsd.org')

child.expect('(?i)name .*: ')
child.sendline('anonymous')
child.expect('(?i)password')
child.sendline('pexpect@sourceforge.net')
child.expect('ftp> ')
child.sendline('cd /pub/OpenBSD/3.7/packages/i386')
child.expect('ftp> ')
child.sendline('bin')
child.expect('ftp> ')
child.sendline('prompt')
child.expect('ftp> ')
child.sendline('pwd')
child.expect('ftp> ')
print("Escape character is '^]'.\n")
sys.stdout.write (child.after)
sys.stdout.flush()
child.interact() # Escape character defaults to ^]
# At this point this script blocks until the user presses the escape character
# or until the child exits. The human user and the child should be talking
# to each other now.

# At this point the script is running again.
print('Left interactve mode.')

if child.isalive():
    child.sendline('bye') # Try to ask ftp child to exit.
    child.close()
# Print the final state of the child. Normally isalive() should be FALSE.
if child.isalive():
    print('Child did not exit gracefully.')
else:
    print('Child exited gracefully.')