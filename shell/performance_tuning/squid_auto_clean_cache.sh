#!/bin/bash 
DIR=/data/cache/ 
Command=/usr/sbin/squidclient 
if 
        [ "$1" = "" ];then 
        echo "Usage:{$0 "\$1" ,Example exec $0 forum.php}" 
        exit 
fi 
grep -r -a $1 ${DIR} | strings | grep "http:"|grep -v "=" >list.txt 
count=`cat list.txt|wc -l` 
if 
        [ "$count" -eq "0" ];then 
        echo -e "---------------------------------\nThe $1 cache already update,Please exit ......"   
        exit 
fi 
while read line 
do 
        $Command -m PURGE -p 80 "$line" >>/dev/null 
        if [ $? -eq 0 ];then 
        echo -e "----------------------------------\nThe $line cache update successfully!" 
        fi 
done < list.txt 