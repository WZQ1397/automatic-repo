#!/bin/sh
if [[ ! -d /usr/local/logstash ]];
then
    echo "no such dir!"
fi
cp /usr/share/zoneinfo/Asia/Shanghai  /etc/localtime
cp conf/logrotate /etc/logrotate.d/spider
export PYTHONPATH=`pwd` && python bin/timer
echo $1
sleep $1
export PYTHONPATH=`pwd` && python bin/spider
/usr/local/logstash/bin/logstash -f conf/agent.conf
while true;do
    sleep 3600;
    logrotate /etc/logrotate.d/spider -f
done;
