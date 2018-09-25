#!/bin/bash

# Var Define Area
source ./config.ini

function MotdBanner()
{
echo "***************************************************"
echo "* This is Zach JumperServer! Read Follow To Use!  *"
echo "*       1) Select Your Server Environment         *"
echo "*       Follow Choice PRD / DEV / LOCAL           *"
echo "*       2) Select Server Which Groupid Belong     *"
echo "*       3) Select ServerIP To Login               *"
echo "***************************************************"
read -p "Step 1:Select Your Server Environment: " SerEnv
echo $SerEnv
}

## Select Spec Group Hosts
function ActiveHost()
{
    local Groupid=$1
    sql="select host from hosts where hostid IN (select hostid from hosts_groups where groupid=$Groupid) and host like \"%.%.%.%\""
    Cmd="mysql -h $HOST -u$USER -p$AUTH_STRING -P$SQL_PORT $DB"
    res=`$Cmd -e "$sql" | awk 'NR>1' `
    printf "`echo $res | tr ' ' '\n'`"
    echo ""
}

## List Availiable Group
function ListGroup()
{
    count=0
    filename=`mktemp /tmp/test.XXXX`
    rm $filename
    Cmd="mysql -h $HOST -u$USER -p$AUTH_STRING -P$SQL_PORT $DB"
    Sql="select groupid,name from groups where groupid>14;"
    $Cmd -t -e "$Sql" > $filename

    fileinfo=$(cat $filename |awk -F "|" '{print $1,$2,$3}')
    for line in $fileinfo
    do
        Flag=0
        echo $line | sed 's/\.\|-\|+\|%\|\^//g' | grep [0-9a-zA-Z] >/dev/null || Flag=1
        #echo $Flag
        if [ $Flag -eq 0 ];then
            count=$count+1
            printf "  %-8s" $line
            [[ $count -eq 2 ]] && echo "" && count=0
        else
            #   echo ""
            echo $line
        fi
    done
    read -p "Step 2:Select Group You Find: " LogGroup
    echo $LogGroup
}
 
## This is Main function
function Login()
{
	MotdBanner
    ListGroup
    local Env=echo $1 | tr 'A-Z' 'a-z'
    local HostPort=22
    ActiveHost $LogGroup
    if [[ $Env=="prd" ]];
    then
        HostPort=$PRD_HOST_PORT
		Key=$KeyLoc$PrdKeyName
	else
		Key=$KeyLoc$DefKeyName
    fi
	read -p "Step 3:Select Your Hosts To Login:" LogHost
	if [[ $Env=="local" ]];
	then
		ssh $LogHost -p$HostPort
	else
		ssh -i $Key $LogHost -p$HostPort
	fi
	local IP=`who am i| awk '{print $NF}' | sed -e 's/[()]//g'`
	
	## need to verity
	[[ $? -eq 0 ]] && Chk=" Success" || Chk=" Failed"
	echo `date `"Login To " $LogHost $Chk " From " $IP > $RECORD_FILE
}

Login

 
# 
## groups name
#select name from groups where groupid>14;
#
## select all
#select hostid,name from groups A,hosts_groups B where A.groupid=B.groupid and A.groupid>14;
#
## count server
#select count(hostid) from hosts where hostid>10253;
#
## All alive hosts
#select count(available) from hosts where hostid>10253 and available=1; 
#
## show spec group hosts available
#select count(available) from hosts where hostid IN (select hostid from hosts_groups where groupid=15) and available=1;
#
## select spec group hosts
#select host from hosts where hostid IN (select hostid from hosts_groups where groupid=15) and host like "%.%.%.%";
#
