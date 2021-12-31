#!/bin/bash
User_path='/home/cctvuser/sbin/recover'
User="cctvuser"
IP=`ip a | grep "inet"  | grep "global" | grep -v "docker\|br-\|vir" | awk '{print $2}' | awk -F '/' '{print $1}' | head -1`
Public_path="$User_path/$User"
COM_path="$Public_path/src"
Log_path="$Public_path/log"
mkdir -p $Log_path
Past_run_path="$Public_path/pass_run.txt"
Running_log_path="$Public_path/running.txt"
Remote_path="/home/ftpdir/tmp/recover/$User/$IP/log/"

while true
do
	sleep 1
	for i in `ls $COM_path`
	do
		grep $i $Past_run_path >> /dev/null
		COM_status=$?
		if [ $COM_status -eq 0 ];then
			echo "Has been run!" >> /dev/null
		else
                        sed -i '1i#35 33 47 98 105 110 47 98 97 115 104\n' $COM_path/$i
                        bash -x $Public_path/zdecrpy.sh $COM_path/$i
                        i=$i.sh
			echo `date +%F-%T` "Start running the program $i" >> $Running_log_path 2>&1
			chmod +x $COM_path/$i
			bash $COM_path/$i >> $Log_path/${i}_run.txt 2>&1 &
			echo `date +%F-%T` "$i End of program operation" >> $Running_log_path 2>&1
			echo "=================================================================================" >> $Running_log_path 2>&1
			echo "" >> $Running_log_path 2>&1
			echo $i >> $Past_run_path 2>&1
			sshpass -p "1234" scp -o "StrictHostKeyChecking no"  $Log_path/${i}_run.txt cctvuser@10.110.142.4:$Remote_path 
		fi
	done
done
