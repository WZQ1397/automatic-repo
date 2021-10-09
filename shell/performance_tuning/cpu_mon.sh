#!/bin/sh

#定义变量

secs=1800
unit_time=30

stepts=$(( $secs / $unit_time ))

echo CPU usage...;

for((i=0;i<stepts;i++))
do
	    ps -eo comm,pcpu | tail -n +2 >> /tmp/cpu_usage.$$                          #$$表示当前进程pid信息
	        sleep $unit_time
done

	echo CPU eaters:

	cat /tmp/cpu_usage.$$ | \
	awk '{process[$1]+=$2}END{for(i in process){printf("%-20s %s\n",i,process[i])}}' | sort -nrk 2 | head | tee -a /root/cpu_mon.log
	top=`tail /root/cpu_mon.log | head -1 | awk '{print $NF}'`
	if [[ $top -gt 90000 ]];
	then
	   echo "warning"
	   topname=`tail /root/cpu_mon.log | head -1 | awk '{print $1}'`
	   host=`hostname`
	   curl 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=44dbcb66-f788-4170-885c-f0cb52b46ec8' -H 'Content-Type: application/json' -d '{"msgtype": "text","text": {"content": "'$host': '$topname' - CPU USAGE TOO HIGH!"},"mentioned_list":["@all"]}'
	fi
	rm -f /tmp/cpu_usage.$$
