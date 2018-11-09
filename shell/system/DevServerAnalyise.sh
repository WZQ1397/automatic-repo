#!/bin/bash
# Author: Zach.Wang


ServerAnalyise=Service.log
#CMD=($CMD_Basic $CMD_WAR $CMD_JAR)
SSHLists="/root/.ssh/known_hosts"
for Server_IP in `cat $SSHLists | awk '{print $1}' | egrep -v "\[|^[[:alpha:]]" | grep 192`
do
  if [ `echo $Server_IP | grep "\[" | wc -l` -gt 0 ];
  then
    x=${Server_IP#*[}
    Server_IP=${x%]*}
  fi
  echo "#####  " $Server_IP "#####"  >> $ServerAnalyise
  echo -e "Checking Server" $Server_IP"   \c"
  Check=`ssh web@$Server_IP "uptime"`
  Status=$?
  [[ $Status -gt 0 ]] && echo "Error! Server Can Not Be Connected Or Exists!" >> $ServerAnalyise || echo "OK!"
  echo $Check >> $ServerAnalyise
  [[ $Status -gt 0 ]] && continue
  #basic service
#  ssh web@$Server_IP "ps -Ao pid,cmd | awk '\$1>999 {\$1=\"\";print}' | egrep -v \"bash|udevd|sshd|ps|awk|grep|pickup|jbd2|ext|flush|java|tty|acpi|hald\"" >> $ServerAnalyise
  sleep 1
  #war
  #  ssh web@$Server_IP "ps -Ao cmd | grep "logging.config.file" | awk -F "=" '{print \$2}' | awk '{print \$1}' | grep "^/" | awk -F "/conf" '{print \$1}'" >> $ServerAnalyise
  ssh web@$Server_IP ps -Ao pid,command | grep "\/data\/web" | awk -F "-D" '{print $2}' | cut -d "/" -f 4 | egrep -o "([[:alnum:]]+-){2,10}.*" >> $ServerAnalyise
  sleep 1
  #jar
  ssh web@$Server_IP ps -Ao pid,command | grep '\-jar' | awk -F "-jar" '{print $2}' | cut -d "." -f 1 | egrep -o "([[:alnum:]]+-){2,10}.*" >> $ServerAnalyise

  echo "+++++++++++++++++++++++" >> $ServerAnalyise
done
