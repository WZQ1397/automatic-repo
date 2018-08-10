#/bin/bash
#Author: Zach.Wang

DATA=`date -d "1 week ago" +%Y.%m.%d`
cur_time=`date`
LOG_PATH="/tmp/es-index-clear.log"

#删除7天前的日志
curl -XDELETE http://127.0.0.1:9200/*-${DATA}

if [ $? -eq 0 ];then
  echo $cur_time"-->del $DATA log success.." >> $LOG_PATH
else
  echo $cur_time"-->del $DATA log fail.." >> $LOG_PATH
fi

curl -XGET 'http://127.0.0.1:9200/_cat/indices/?v' >> $LOG_PATH
echo "++++++++++++++++++" >> $LOG_PATH