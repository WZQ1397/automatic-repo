#!/bin/bash
# Function:     检查使用共享表空间的表结果存放在/tmp/checkresult.txt


dbpath="/var/lib/mysql"  #输入实例所在路径
dbs=`ls -d $dbpath/*/`   #输入要检查的数据库
>/tmp/checkresult.txt


#备份
for db in $dbs
do

    cd  ${dbpath}${db}
    echo --------------${db}--------------- >> /tmp/checkresult.txt
    for i in `ls *.frm`
    do
        p=`echo $i|awk -F'.frm'  '{print $1}'`

    if [ ! -s $p.ibd ]
    then
        echo $p >> /tmp/checkresult.txt
    fi
    done
    echo   >> /tmp/checkresult.txt

done