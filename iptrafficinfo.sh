#!/bin/bash  
#        Author: Zach.Wang
#        Create: 2017-04-06 10:15:59

INTERVAL="1"  # update interval in seconds  
if [ -z "$1" ]; then  
        echo  
        echo usage: $0 [network-interface]  
        echo  
        echo e.g. $0 eth0  
         echo  
         exit  
fi  
IF=$1  
while true  
do  
	R1=`cat /sys/class/net/$1/statistics/rx_bytes`  
    T1=`cat /sys/class/net/$1/statistics/tx_bytes`  
    sleep $INTERVAL  
    R2=`cat /sys/class/net/$1/statistics/rx_bytes`  
    T2=`cat /sys/class/net/$1/statistics/tx_bytes`  
    TBPS=`expr $T2 - $T1`  
    RBPS=`expr $R2 - $R1`  
    TKBPS=`expr $TBPS / 1024`  
    RKBPS=`expr $RBPS / 1024`  
    echo "TX $1: $TKBPS kb/s RX $1: $RKBPS kb/s"  
done
