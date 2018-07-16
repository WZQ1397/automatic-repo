#!/bin/bash
# $1: A1 or B1  $2: PACKAGE ARGUMENTS

DATEYEAR=`date +%Y`
MONTH=`date +%m`
DATE=`date -d '-1 month' '+%Y-%m'`
REGION=$1
PACKAGE=$2
REMOTE_HOST=172.10.10.28

if [ $MONTH -eq 01 ];then
   DATEYEAR=$[$DATEYEAR-1]
fi 

LOG_DIR=/data/tsjinrong/logs/$PACKAGE/
LOG_BAK_DIR=/data/logs_backup/$PACKAGE/$DATEYEAR/
REMOTE_DIR=/data/logs_backup/$PACKAGE/$DATEYEAR/

if [ ! -e $LOG_BAK_DIR ]; then
		mkdir -p $LOG_BAK_DIR
fi

if [ $# -eq 2 ] && [ $1 == "A1" -o $1 == "B1" ]; then

				# gzip
				cd $LOG_DIR
				/bin/tar zcf $LOG_BAK_DIR/${PACKAGE}.log-${DATE}-${REGION}-bak.tar.gz ${PACKAGE}.log.${DATE}*

				# scp
				ssh $REMOTE_HOST "if [ ! -e $REMOTE_DIR ]; then mkdir -p $REMOTE_DIR; fi"
				scp $LOG_BAK_DIR/${PACKAGE}.log-${DATE}-${REGION}-bak.tar.gz $REMOTE_HOST:${REMOTE_DIR}

else

		   echo "Usage `basename $0` {A1 PACKAGE_NAME|B1 PACKAGE_NAME}"
		   
fi