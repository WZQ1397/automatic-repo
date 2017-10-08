#!/bin/bash
#
echo "COUNT CPU HEX"
[ $# -ne 1 ] && echo ‘$1 is Cpu core number’ && exit 1
CCN=$1
echo “Print eth0 affinity”
for((i=0; i<${CCN}; i++))
do
echo ==============================
echo "Cpu Core $i is affinity"
((affinity=(1<<i)))
echo "obase=16;${affinity}" | bc
done