#!/bin/sh
while true 
do
   num=`cat site.log|wc -l`
   md5num=`md5sum -c /tmp/checkmd5.db|grep -i FAILED|wc -l`
   filenum=`ls -l /etc/ |wc -l`
   if [  $md5num -ne 0 ]
   then
      echo "`md5sum -c /tmp/checkmd5.db|grep -i FAILED`"
   fi

   if [ $filenum -ne $num ]
   then
      echo "/etc/ dir is change"
   fi
   sleep 5
done
