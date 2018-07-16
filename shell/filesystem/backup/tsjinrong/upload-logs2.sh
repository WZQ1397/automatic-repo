#!/bin/bash
DATEYear=`date "+%Y"`
MONTH=`date +%m`
DATEBeforMonth=`date -d '1 month ago' +%Y-%m`
Applogsdir=/data/logs_backup
cnnorth1a=$1
cnnorth1b=$2
Apply="approval-admin,approval-esb,account-admin,account-esb,payment-admin,payment-esb,snowflake-admin,snowflake-esb,product-esb,auth-esb,appLend-admin,appLend-esb,appLend-data-esb,payAuth-es
b,payable-admin,applend-entry"

if [ $MONTH -eq 01 ];then
   DATEYear=$[$DATEYear-1]
fi

#upload Apply

for App in `echo $Apply | sed 's/,/ /g'`;do

#if [ $# -eq 2 ];then
#if [ $# -eq 2 ] && [ $1 == 'A1' -o $1 == 'B1' ] && [ $2 == 'A1' -o $2 == 'B1' ];then
if [ $# -eq 2 ] && ([ $1 == 'A1' -a $2 == 'B1' ] || [ $1 == 'B1' -a $2 == 'A1' ]);then
		cd ${Applogsdir}/${App}/${DATEYear}
		/usr/local/bin/aws s3 cp ./${App}.log-${DATEBeforMonth}-${cnnorth1a}-bak.tar.gz  s3://approval.logs.backup/${App}/${DATEYear}/
		/usr/local/bin/aws s3 cp ./${App}.log-${DATEBeforMonth}-${cnnorth1b}-bak.tar.gz  s3://approval.logs.backup/${App}/${DATEYear}/

else
		echo "Usage ARG: A1 B1"
		exit 1
fi

done
