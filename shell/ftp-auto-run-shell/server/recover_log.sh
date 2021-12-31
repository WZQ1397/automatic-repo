#!/bin/bash
basepath=$(cd `dirname $0`; pwd)
clist

while true
do
   flag=$(cat $basepath/flag.txt)
   echo ""
   echo `date`, $flag

   if [ "$flag" = "true" ];
   then

   for user in "cctvuser" "root"
   do

   echo $user root

      for ip in "1" "2" "3" "4" "33" "34" "35" "36" "37" "38" "41"
      do
          echo $user 10.110.142.$ip
          if [ "$ip" = "41" ];
          then
              pd="UIOP"
          else
              pd="1234"
          fi

          /usr/bin/sshpass -p $pd rsync -t -r -e "ssh -o StrictHostKeyChecking=no" cctvuser@10.110.142.$ip:/home/cctvuser/sbin/recover/$user/log /home/ftpdir/tmp/recover/$user/10.110.142.$ip/
          chmod -R 777 $basepath
      done

   done

   fi

   sleep 1s

done