#!/bin/bash

Host="172.16.6.220"
User="root"
Passwd="edong"
Mysql="/usr/bin/mysql"
Cmd="show slave status"
Dir="/Mysql_Status_py"

$Mysql -u $User -p"$Passwd" -h $Host -e "show slave status\G" > $Dir/slave.txt



SLAVE_SQL_RUNNING=$(cat "$Dir"/slave.txt | grep "Slave_SQL_Running:" | awk '{print $NF}')
SLAVE_IO_RUNNING=$(cat "$Dir"/slave.txt | grep "Slave_IO_Running:" | awk '{print $NF}')
if [ $SLAVE_IO_RUNNING == $SLAVE_SQL_RUNNING ];then
	Res="0"
else
	Res="1"
fi
