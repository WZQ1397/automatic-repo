#!/bin/bash
# Author: Zach.Wang
# Usage Clean_Log.sh TIME
DAYS=$1
MongoConf="/etc/mongod.conf"
LOG_NAME="MongoDB_Clear"
MongoDefPath="/data/db/"

if [ -f $MongoConf ];
then
  CLEAN_PATH=`grep "dbPath" $MongoConf | awk -F ":" '{print $2 }'`
else
  [[ -d $MongoDefPath ]] && CLEAN_PATH=$MongoDefPath || echo "No Data dir!"
fi

cd $CLEAN_PATH
if [[ " "`pwd`"/" == $CLEAN_PATH && $DAYS -ge 3 ]];
then
  find -ctime +$DAYS | xargs rm -rf \{};
  echo $CLEAN_PATH "CLEAN SUCCESS!" date >> /tmp/$LOG_NAME.log
else
  echo $CLEAN_PATH "CLEAN failed!" date >> /tmp/$LOG_NAME.log
fi
echo "+++++++++++++++++++++++" >> /tmp/$LOG_NAME.log
