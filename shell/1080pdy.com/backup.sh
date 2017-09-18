#!/bin/bash
var=$(uptime | cut -d ':' -f 5 | cut -d ',' -f 2);
bkdate=$(date | cut -d " " -f 2,3,6 | sed  's/ /-/g');
if [[ `expr $var \< 3` ]];
then 
tar -zcf /data/backup/$bkdate.tar.gz /data/wwwroot/1080pdy.com/ -C /data/wwwroot/
echo "backup success! `date `" >> /data/1080pdy.log
else
echo "backup failed! `date` " >> /data/1080pdy.log
fi
