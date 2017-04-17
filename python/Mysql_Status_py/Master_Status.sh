#!/bin/bash

Host="172.16.6.231"
User="root"
Passwd="edong"
Mysql="/usr/bin/mysql"
Cmd="show master status"
Dir="/Mysql_Status_py"

$Mysql -u $User -p"$Passwd" -h $Host -e "show master status" > $Dir/master.txt
num=`sed -n '2p' "$Dir"/master.txt | awk '{print $2}'`
