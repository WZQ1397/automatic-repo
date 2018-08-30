#!/bin/bash 
#0 4 * * * sh /usr/local/script/filebak.sh > /dev/null 2>&1
# backup auto and transmit file to backup server 
SRC_PATH="/data/newweb/webapps/ /data/newweb/conf/ /data/newweb/work/"
DST_PATH=/data/backup/
REMOTE_SERVER="root@192.168.36.24:/backup/"
BAK_NAME=newweb

OldFile="$DST_PATH""$BAK_NAME"_$(date +%y%m%d --date='3 month ago').tar.gz
LogFile="$DST_PATH""$BAK_NAME".log."$(date +%y%m)"
NewFile="$DST_PATH""$BAK_NAME"_$(date +%y%m%d).tar.gz
#FileNUM=$(find "$SRC_PATH" -type f -print | wc -l)

echo "-------------------------------------------" >> $LogFile 
echo $(date +"%y-%m-%d %H:%M:%S") >> $LogFile 
echo "--------------------------" >> $LogFile 

#Delete Old File 
if [ -f $OldFile ] 
then 
   rm -f $OldFile >>$LogFile 2>&1 
   echo "[$OldFile]Delete Old File Success!" >> $LogFile 
else 
   echo "[$OldFile]No Old Backup File!" >> $LogFile 
fi

if [ -f $NewFile ] 
then 
   echo "File has backuped Successfully!"
else 
   tar czf $NewFile $SRC_PATH>>$LogFile 2>&1
   echo "[$NewFile]Backup Success!" >> $LogFile
#  echo "[$FileNUM] files Backuped!" >> $LogFile
fi
scp $NewFile $REMOTE_SERVER>> $LogFile
if [ $? -eq 0 ]
then
   echo "[$NewFile] transmit Success!" >> $LogFile
else
   echo "[$NewFile] transmit Failed!!!" >> $LogFile
fi
fintime=$(date +"%y-%m-%d %H:%M:%S")
echo "---------- $fintime finished ----------" >> $LogFile
