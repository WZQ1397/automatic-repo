#!/bin/bash  
#AUTHOR: Zach.Wang
#Usage: Tomcat7To8.sh $MigrateDirName
DATA_DIR="/data/web/"
TOMCAT_SRC=$1
target_pattern="tomcat8-"
subfix=`awk -F "tomcat-" '{print $2}' `
TOMCAT_DST=$target_pattern-$subfix

CHANGE_LIST="
conf/context.xml
conf/server.xml
bin/startup.sh
bin/shutdown.sh
"
cd $DATA_DIR
for Lst in $CHANGE_LIST
do
	cat /data/web/$TOMCAT_SRC/$Lst > $DATA_DIR/$TOMCAT_DST/$Lst
done
sed -i '/org.apache.catalina.core.JasperListener/d' $DATA_DIR/$TOMCAT_DST/conf/server.xml
sed -i '/tomcat-/$target_pattern/g' $DATA_DIR/$TOMCAT_DST/bin/startup.sh
sed -i '/tomcat-/$target_pattern/g' $DATA_DIR/$TOMCAT_DST/bin/shutdown.sh

/bin/bash $TOMCAT_SRC/bin/shutdown.sh
sleep 5
prog=`ps -Ao pid,command | grep $TOMCAT_SRC`
[[ `echo $prog | wc -l ` -ge 2 ]] && flag=1
[[ flag ]] && kill -9 `echo $prog | grep -v "grep" | awk '{print $1}'`

/bin/bash $TOMCAT_SRC/bin/startup.sh
sleep 5
ps -Ao pid,command | grep $TOMCAT_DST
tail -50 $TOMCAT_DST/log/catalina.out




