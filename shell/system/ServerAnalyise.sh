#!/bin/bash
# Author: Zach.Wang

#Define Postion To Save Record 
ServerAnalyise=Service.log
#CMD=($CMD_Basic $CMD_WAR $CMD_JAR)

#Define SSHLists
SSHLists="/root/.ssh/known_hosts"

#If you want to use User custom HostList, please replace in AREA!
for Server_IP in `cat $SSHLists | awk '{print $1}' | egrep "^\[*|^[[:digit:]]+"`
do
  # Check Not default SSH port Server EG:[172.10.98.105]:9622
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
  ssh web@$Server_IP "ps -Ao pid,cmd | awk '\$1>999 {\$1=\"\";print}' | egrep -v \"bash|udevd|sshd|ps|awk|grep|pickup|jbd2|ext|flush|java|tty|acpi|hald\"" >> $ServerAnalyise
  sleep 1
  #war
  ssh web@$Server_IP "ps -Ao cmd | grep "logging.config.file" | awk -F "=" '{print \$2}' | awk '{print \$1}' | grep "^/" | awk -F "/conf" '{print \$1}'" >> $ServerAnalyise
  sleep 1
  #jar
  ssh web@$Server_IP "ps -Ao cmd | grep '\-jar' | awk -F 'jar' '{print \$2}'" | grep -v awk >> $ServerAnalyise

  echo "+++++++++++++++++++++++" >> $ServerAnalyise
done
