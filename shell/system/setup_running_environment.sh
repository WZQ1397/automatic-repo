#!/bin/sh

TX_QUEUELEN_MAX=1000000
NF_CONNTRACK_MAX=1000000
NF_CONNTRACK_TIMEOUT_MAX=7200
IP_DEFAULT_TTL=253
MEM_MAX=6553600
DEBUG="0"

[ "$2" = "debug" ] && { DEBUG="1";}

print_debug()
{
	[ "$DEBUG" = "1" ] && { echo -e "$*";}
}

compare_version()
{
         VAR_1_PREFIX=${1%%.*}
         VAR_1_POSTFIX=${1:${#VAR_1_PREFIX} + 1}
         VAR_2_PREFIX=${2%%.*}
         VAR_2_POSTFIX=${2:${#VAR_2_PREFIX} + 1}
         while [ "$VAR_1_PREFIX" != "" -a "$VAR_2_PREFIX" != "" ];do
                   [ "$VAR_1_PREFIX" -gt "$VAR_2_PREFIX" ] && { return 1;}
                   [ "$VAR_1_PREFIX" -lt "$VAR_2_PREFIX" ] && { return 255;}
                   VAR_1_PREFIX=${VAR_1_POSTFIX%%.*}
                   VAR_1_POSTFIX=${VAR_1_POSTFIX:${#VAR_1_PREFIX} + 1}
                   VAR_2_PREFIX=${VAR_2_POSTFIX%%.*}
                   VAR_2_POSTFIX=${VAR_2_POSTFIX:${#VAR_2_PREFIX} + 1}
         done
         [ "$VAR_1_PREFIX" = "$VAR_2_PREFIX" ] && { return 0;}
         [ "$VAR_1_PREFIX" = "" ] && { return 255;}
         [ "$VAR_1_PREFIX" = "$VAR_2_PREFIX" ] && { return 1;}
}
get_kernel_version()
{
	KERNELNUMBER=`uname -r`
	KERNELNUMBER=${KERNELNUMBER%-*}
	echo $KERNELNUMBER
}
get_eth_driver()
{
	ethtool -i $1 | grep driver | cut -d' ' -f2
}
get_eth_driver_version()
{
	ethtool -i $1 | grep version -m1 | cut -d' ' -f2
}
set_sysctl()
{
	PROC_NAME=/proc/sys/${1//./\/}
	print_debug "  Set $1 $2"
	if [ -e $PROC_NAME ]; then
		echo $2 > $PROC_NAME
	fi
	if [ "`grep "$1" /etc/sysctl.conf 2>/dev/null`" == "" ]; then
		echo "$1 = $2" >> /etc/sysctl.conf
	else
		sed -i -e "/$1/c $1 = $2" /etc/sysctl.conf
	fi
}
check_network()
{
	print_debug "  Close iptables"
	/etc/init.d/iptables stop > /dev/null 2>&1
	/etc/init.d/ip6tables stop > /dev/null 2>&1
	chkconfig iptables off > /dev/null 2>&1
	chkconfig ip6tables off > /dev/null 2>&1

	set_sysctl net.ipv4.conf.all.arp_announce 2
	set_sysctl net.ipv4.conf.all.arp_ignore 1
	set_sysctl net.ipv4.conf.all.rp_filter 0

	set_sysctl net.ipv4.ip_default_ttl $IP_DEFAULT_TTL
	compare_version "2.6.18" $(get_kernel_version)
	if [ $? -eq 255 ]; then
		set_sysctl net.netfilter.nf_conntrack_max $NF_CONNTRACK_MAX
		set_sysctl net.netfilter.nf_conntrack_tcp_timeout_established $NF_CONNTRACK_TIMEOUT_MAX
	else
		set_sysctl net.ipv4.netfilter.ip_conntrack_max  $NF_CONNTRACK_MAX
		set_sysctl net.ipv4.netfilter.ip_conntrack_tcp_timeout_established $NF_CONNTRACK_TIMEOUT_MAX
	fi
	set_sysctl net.core.wmem_max $MEM_MAX
	set_sysctl net.core.wmem_default $MEM_MAX
	set_sysctl net.core.rmem_max $MEM_MAX
	set_sysctl net.core.rmem_default $MEM_MAX

	ETHS=`ip link show|grep "mtu"|grep -v "lo"|grep -v "bond"|awk '{print $2}'|cut -d ':' -f1`
	for ETH in $ETHS
	do 
		ETH_DRIVER_NAME=$(get_eth_driver $ETH)
		ETH_DRIVER_VERSION=$(get_eth_driver_version $ETH)
		if [ -x "if_$ETH_DRIVER_NAME.sh" ]; then
			. ./if_$ETH_DRIVER_NAME.sh $ETH_DRIVER_VERSION $ETH
		fi
		print_debug "  Set $ETH txqueuelen $TX_QUEUELEN_MAX"
		print_debug "  Set $ETH autoneg off rx off tx off"
		print_debug "  Set $ETH rp_filter 0"
		if [ -f /etc/SuSE-release ]; then
			. ./ifup_local.sh $ETH_DRIVER_VERSION $ETH
		else
			. ./ifup_local.sh $ETH
		fi
	done
}

check_permission()
{
	if [ `whoami` != "root" ];then
		echo "  Need root permission."
		exit 1
	fi
}

check_permission
check_network

if [ /etc/init.d/irqbalance ];then
     /etc/init.d/irqbalance stop > /dev/null 2>&1
     chkconfig --del irqbalance > /dev/null 2>&1
     print_debug "  Irqbalance disabled"
fi

