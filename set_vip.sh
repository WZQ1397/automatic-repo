#!/bin/bash
#        Author: Zach.Wang
#        Create: 2017-04-05 16:37:24
#        HOW TO USE
#./set_vip.sh start 192.168.1.100 

case $1 in
start)
echo 1 > /proc/sys/net/ipv4/conf/all/arp_ignore
echo 1 > /proc/sys/net/ipv4/conf/lo/arp_ignore
echo 2 > /proc/sys/net/ipv4/conf/all/arp_announce
echo 2 > /proc/sys/net/ipv4/conf/lo/arp_announce
ifconfig lo:0 $vip netmask 255.255.255.255 broadcast $vip
route add -host $vip dev lo:0
;;
stop)
echo 0 > /proc/sys/net/ipv4/conf/all/arp_ignore
echo 0 > /proc/sys/net/ipv4/conf/lo/arp_ignore
echo 0 > /proc/sys/net/ipv4/conf/all/arp_announce
echo 0 > /proc/sys/net/ipv4/conf/lo/arp_announce
ifconfig lo:0 del $vip
;;
status)

# Status of LVS-DR real server.
islothere=`/sbin/ifconfig lo:0 | grep $VIP`
isrothere=`netstat -rn | grep ¡°lo:0¡å | grep $VIP`
if [ ! "$islothere" -o ! "isrothere" ];then
# Either the route or the lo:0 device
# not found.
echo ¡°LVS-DR real server Stopped.¡±
else
echo ¡°LVS-DR Running.¡±
fi
;;
*|help)
echo ¡°$0: Usage: $0 {start|status|stop}¡±
exit 1
;;
esac
