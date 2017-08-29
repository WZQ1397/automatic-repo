#!/bin/bash 
# 
# The interface that connect Internet
# echo 
echo "Enable IP Forwarding..." 
echo 1 > /proc/sys/net/ipv4/ip_forward 
echo "Starting iptables rules..."

IFACE="eth0"

# include module 
modprobe ip_tables 
modprobe iptable_nat 
modprobe ip_nat_ftp 
modprobe ip_nat_irc 
modprobe ip_conntrack 
modprobe ip_conntrack_ftp 
modprobe ip_conntrack_irc 
modprobe ipt_MASQUERADE

# init 
/sbin/iptables -F 
/sbin/iptables -X 
/sbin/iptables -Z 
/sbin/iptables -F -t nat 
/sbin/iptables -X -t nat 
/sbin/iptables -Z -t nat
/sbin/iptables -X -t mangle
# drop all 
/sbin/iptables -P INPUT DROP 
/sbin/iptables -P FORWARD ACCEPT 
/sbin/iptables -P OUTPUT ACCEPT 
/sbin/iptables -t nat -P PREROUTING ACCEPT 
/sbin/iptables -t nat -P POSTROUTING ACCEPT 
/sbin/iptables -t nat -P OUTPUT ACCEPT

/sbin/iptables -A INPUT -f -m limit --limit 100/sec --limit-burst 100 -j ACCEPT 
/sbin/iptables -A INPUT -p tcp -m tcp --tcp-flags SYN,RST,ACK SYN -m limit --limit 20/sec --
limit-burst 200 -j ACCEPT
/sbin/iptables -A INPUT -p icmp -m limit --limit 12/min --limit-burst 2 -j DROP
/sbin/iptables -A FORWARD -f -m limit --limit 100/sec --limit-burst 100 -j ACCEPT 
/sbin/iptables -A FORWARD -p tcp -m tcp --tcp-flags SYN,RST,ACK SYN -m limit --limit 20/sec --
limit-burst 200 -j ACCEPT
/sbin/iptables -A INPUT -i eth1 -p tcp -m tcp -dport 80 -m state -state NEW -m recent -update -seconds 60 -hitcount 20 -name DEFAULT -rsource -j DROP
/sbin/iptables -A INPUT -i eth1 -p tcp -m tcp -dport 80 -m state -state NEW -m recent -set -name DEFAULT -rsource
/sbin/iptables -A INPUT -p tcp -dport 80 -m connlimit  -connlimit-above 30 -j REJECT
/sbin/iptables -A INPUT -p tcp -syn -m connlimit -connlimit-above 20 -j DROP

# open ports 
/sbin/iptables -A INPUT -i $IFACE -p tcp --dport 21 -j ACCEPT 
/sbin/iptables -A INPUT -i $IFACE -p tcp --dport 22 -j ACCEPT 
/sbin/iptables -A INPUT -i $IFACE -p tcp --dport 25 -j ACCEPT 
/sbin/iptables -A INPUT -i $IFACE -p tcp --dport 53 -j ACCEPT 
/sbin/iptables -A INPUT -i $IFACE -p udp --dport 53 -j ACCEPT 
/sbin/iptables -A INPUT -i $IFACE -p tcp --dport 80 -j ACCEPT 
/sbin/iptables -A INPUT -i $IFACE -p tcp --dport 100 -j ACCEPT 
/sbin/iptables -A INPUT -i $IFACE -p tcp --dport 113 -j ACCEPT

# close ports 
iptables -I INPUT -p udp --dport 69 -j DROP 
iptables -I INPUT -p tcp --dport 135 -j DROP
iptables -I INPUT -p udp --dport 135 -j DROP 
iptables -I INPUT -p tcp --dport 136 -j DROP
iptables -I INPUT -p udp --dport 136 -j DROP 
iptables -I INPUT -p tcp --dport 137 -j DROP
iptables -I INPUT -p udp --dport 137 -j DROP 
iptables -I INPUT -p tcp --dport 138 -j DROP
iptables -I INPUT -p udp --dport 138 -j DROP 
iptables -I INPUT -p tcp --dport 139 -j DROP
iptables -I INPUT -p udp --dport 139 -j DROP 
iptables -I INPUT -p tcp --dport 445 -j DROP
iptables -I INPUT -p udp --dport 445 -j DROP 
iptables -I INPUT -p tcp --dport 593 -j DROP
iptables -I INPUT -p udp --dport 593 -j DROP 
iptables -I INPUT -p tcp --dport 1068 -j DROP 
iptables -I INPUT -p udp --dport 1068 -j DROP 
iptables -I INPUT -p tcp --dport 4444 -j DROP 
iptables -I INPUT -p udp --dport 4444 -j DROP 
iptables -I INPUT -p tcp --dport 5554 -j DROP 
iptables -I INPUT -p tcp --dport 1434 -j DROP 
iptables -I INPUT -p udp --dport 1434 -j DROP 
iptables -I INPUT -p tcp --dport 2500 -j DROP 
iptables -I INPUT -p tcp --dport 5800 -j DROP 
iptables -I INPUT -p tcp --dport 5900 -j DROP 
iptables -I INPUT -p tcp --dport 6346 -j DROP 
iptables -I INPUT -p tcp --dport 6667 -j DROP 
iptables -I INPUT -p tcp --dport 9393 -j DROP
iptables -I FORWARD -p udp --dport 69 -j DROP 
iptables -I FORWARD -p tcp --dport 135 -j DROP 
iptables -I FORWARD -p udp --dport 135 -j DROP 
iptables -I FORWARD -p tcp --dport 136 -j DROP 
iptables -I FORWARD -p udp --dport 136 -j DROP 
iptables -I FORWARD -p tcp --dport 137 -j DROP 
iptables -I FORWARD -p udp --dport 137 -j DROP 
iptables -I FORWARD -p tcp --dport 138 -j DROP 
iptables -I FORWARD -p udp --dport 138 -j DROP 
iptables -I FORWARD -p tcp --dport 139 -j DROP 
iptables -I FORWARD -p udp --dport 139 -j DROP 
iptables -I FORWARD -p tcp --dport 445 -j DROP 
iptables -I FORWARD -p udp --dport 445 -j DROP 
iptables -I FORWARD -p tcp --dport 593 -j DROP 
iptables -I FORWARD -p udp --dport 593 -j DROP 
iptables -I FORWARD -p tcp --dport 1068 -j DROP 
iptables -I FORWARD -p udp --dport 1068 -j DROP 
iptables -I FORWARD -p tcp --dport 4444 -j DROP 
iptables -I FORWARD -p udp --dport 4444 -j DROP 
iptables -I FORWARD -p tcp --dport 5554 -j DROP 
iptables -I FORWARD -p tcp --dport 1434 -j DROP 
iptables -I FORWARD -p udp --dport 1434 -j DROP 
iptables -I FORWARD -p tcp --dport 2500 -j DROP 
iptables -I FORWARD -p tcp --dport 5800 -j DROP 
iptables -I FORWARD -p tcp --dport 5900 -j DROP 
iptables -I FORWARD -p tcp --dport 6346 -j DROP 
iptables -I FORWARD -p tcp --dport 6667 -j DROP 
iptables -I FORWARD -p tcp --dport 9393 -j DROP
/sbin/iptables -A INPUT -i $IFACE -m state --state RELATED,ESTABLISHED -j ACCEPT
/sbin/iptables -A INPUT -i $IFACE -m state --state NEW,INVALID -j DROP

# drop ping 
/sbin/iptables -A INPUT -p icmp -j DROP
/sbin/iptables -I INPUT -s 222.182.40.241 -j DROP