#!/bin/bash
local=$1
remote=$2
public=$3
subnetlist=$4
node=$5
function deploy(){
modprobe ip_gre
lsmod |grep ip_gre 
ip tunnel add tun1 mode gre remote $public local $local
ip link set tun1 up
if [[ typeset -u node == "LEFT" ]];then
	ip addr add 192.168.1.1 peer 192.168.1.2 dev tun1
else
	ip addr add 192.168.1.2 peer 192.168.1.1 dev tun1
fi
route add -net $subnetlist dev tun1
echo 1 > /proc/sys/net/ipv4/ip_forward
route -n
ip a
}

deploy

## VPC A
#ip tunnel add tun1 mode gre remote 47.111.177.15 local 10.0.1.77
#ip link set tun1 up
#ip addr add 192.168.1.1 peer 192.168.1.2 dev tun1
#route add -net 172.16.0.0/16 dev tun1
#echo 1 > /proc/sys/net/ipv4/ip_forward
#
## VPC B
#ip tunnel add tun1 mode gre remote 118.31.123.127 local 172.16.101.191
#ip link set tun1 up
#ip addr add 192.168.1.2 peer 192.168.1.1 dev tun1
#route add -net 10.0.1.0/24 dev tun1
#echo 1 > /proc/sys/net/ipv4/ip_forward