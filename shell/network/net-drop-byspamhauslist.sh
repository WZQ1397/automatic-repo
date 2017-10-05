#!/bin/bash

#Script to add firewall rules to a linux system to completely block
#all traffic to and from networks in the spamhaus drop list.

cd /var/lib/
rm -rf /var/lib/drop.list
wget https://www.spamhaus.org/drop/drop.txt
sleep 30
# ./net-drop /var/lib/drop.txt

#While the DROP file should be regularly updated, this should 
#probably be about once per day or less frequently; do _not_ 
#download DROP more than once an hour.

if [ -n "$1" ]; then
	DropList="$1"
else
	DropList="/var/lib/drop.txt"
fi
if [ ! -s "$DropList" ]; then
	echo "Unable to find drop list file $DropList .  Perhaps do:" >&2
	echo "exiting." >&2
	exit 1
fi

if [ ! -x /sbin/iptables ]; then
	echo "Missing iptables command line tool, exiting." >&2
	exit 1
fi

cat "$DropList" \
 | sed -e 's/;.*//' \
 | grep -v '^ *$' \
 | while read OneNetBlock ; do
	/sbin/iptables -I INPUT -s "$OneNetBlock" -j DROP
	/sbin/iptables -I OUTPUT -d "$OneNetBlock" -j DROP
	/sbin/iptables -I FORWARD -s "$OneNetBlock" -j DROP
	/sbin/iptables -I FORWARD -d "$OneNetBlock" -j DROP
done