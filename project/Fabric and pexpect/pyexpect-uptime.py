from __future__ import unicode_literals
import pexpect
import re

# Note that, for Python 3 compatibility reasons, we are using spawnu and
# importing unicode_literals (above). spawnu accepts Unicode input and
# unicode_literals makes all string literals in this script Unicode by default.
p = pexpect.spawnu('uptime')

# This parses uptime output into the major groups using regex group matching.
p.expect('up\s+(.*?),\s+([0-9]+) users?,\s+load averages?: ([0-9]+\.[0-9][0-9]),?\s+([0-9]+\.[0-9][0-9]),?\s+([0-9]+\.[0-9][0-9])')
duration, users, av1, av5, av15 = p.match.groups()

days = '0'
hours = '0'
mins = '0'
if 'day' in duration:
    p.match = re.search('([0-9]+)\s+day',duration)
    days = str(int(p.match.group(1)))
if ':' in duration:
    p.match = re.search('([0-9]+):([0-9]+)',duration)
    hours = str(int(p.match.group(1)))
    mins = str(int(p.match.group(2)))
if 'min' in duration:
    p.match = re.search('([0-9]+)\s+min',duration)
    mins = str(int(p.match.group(1)))

# Print the parsed fields in CSV format.
print('days, hours, minutes, users, cpu avg 1 min, cpu avg 5 min, cpu avg 15 min')
print('%s, %s, %s, %s, %s, %s, %s' % (days, hours, mins, users, av1, av5, av15))