#!/bin/bash
cat >> /etc/bashrc << EOF
HISTDIR='/.auditlog/'
LOGFILE="$HISTDIR`date +%Y%m`.log"
if [ ! -f $LOGFILE ];then
touch $LOGFILE
chmod 777 $LOGFILE
chmod o+t $LOGFILE
fi
USER_IP=`who -u am i 2>/dev/null| awk '{print $NF}'|sed -e 's/[()]//g'` 
export HISTTIMEFORMAT="[%F %T][`whoami`][${USER_IP}] " 
export PROMPT_COMMAND='history 1|tail -1 >> $LOGFILE'

EOF
source /etc/bashrc
