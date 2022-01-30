#!/bin/bash
#Author: Zach.wang
##################### CONFIG START #####################

thld=$1
thld=${thld:-10}
IFS=' '
basepath=`dirname $0`
bannedlist=$basepath"/ipban.list"
logpath=$basepath"/openssh/current"

#####################  CONFIG END  #####################

res=`grep  -oE " ([0-9]{1,3}.){3}[0-9]{1,3} " $logpath | sed 's/ //g' |sort -n|uniq -c`;
#echo $res | awk -F ' ' '{print $1}'
iplist=(`echo $res | awk  -F ' ' -v thld=$thld 'BEGIN{limit=thld}{if($1>=limit){printf $NF" "}}' `)
#IFS='\n'
[[ ${#iplist[@]} -eq 0 ]] && echo "No IP need to be banned!"
for ip in ${iplist[@]};
do
	grep -q $ip $bannedlist
	if [[ $? -eq 0 ]];
	then
	   echo $ip has been banned!
	   continue
	fi

	echo $ip | tee -a $banedlist
	echo "iptables -A INPUT -s $ip/32 -j DROP  -m comment --comment \"auto drop\""
	echo "iptables -A OUTPUT -d $ip/32 -j DROP  -m comment --comment \"auto drop\""
	iptables -A INPUT -s $ip/32 -j DROP  -m comment --comment "auto drop"
	iptables -A OUTPUT -d $ip/32 -j DROP  -m comment --comment "auto drop"
done
