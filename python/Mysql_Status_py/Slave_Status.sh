#!/bin/bash

Host="172.16.6.220"
User="root"
Passwd="edong"
Mysql="/usr/bin/mysql"
Cmd="show slave status"
Dir="/Mysql_Status_py"

res=$(cat "$Dir"/slave.txt  | grep "Read_Master_Log_Pos:" | awk '{print $NF}')
