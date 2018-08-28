#!/bin/bash
# Usage Clean_Log.sh PATH TIME
DAYS=$2
CLEAN_PATH=$1

cd $CLEAN_PATH
if [[ `pwd` == $CLEAN_PATH && $DAYS -ge 3 ]];
then
  find -ctime +$DAYS | xargs rm -rf \{};
  echo $CLEAN_PATH "CLEAN SUCCESS!" date >> /tmp/zach_clean.log
else
  echo $CLEAN_PATH "CLEAN failed!" date >> /tmp/zach_clean.log
fi
echo "+++++++++++++++++++++++" >> /tmp/zach_clean.log
sleep 30
> catalina.out
