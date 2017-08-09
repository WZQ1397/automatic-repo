#!/bin/bash

flag=0
user=root
pass=123456

mysql -u$user -p"$pass" -e "show databases;" &>/dev/null
[ $? -ne 0  ] && read -p "Mysql do not running,start it?(`echo -e "\033[32myes/no\033[0m"`):" choice && flag=1
[[ "choice" -eq "yes" ]] && service mysqld start &>/dev/null && flag=0
[ $flag -eq 1 ] && exit 2
database=`mysql -u$user -p$pass  -e "show databases;"|sed 1d|grep -v 'schema'`

echo -e "\033[32m==================backup start=====================\033[0m"
for i in $database
do
  tables=`mysql -u$user -p"$pass" -e "use $i;show tables;"|sed 1d`
  for j in $tables
  do
    mysqldump -u$user -p"$pass"   -B --databases $i --tables $j > /tmp/${i}-${j}-`date +%F`.sql
   [ $? -eq 0 ] && echo $i $j ok >>/tmp/table.log||echo $i $j failed >>/tmp/table.log
   [ $? -eq 0 ] && echo -e "$i $j \033[32mok\033[0m" ||echo -e "$i $j \033[31mfailed\033[0m"
  done

done
echo -e "\033[32m===================backup stop=======================\033[0m"
