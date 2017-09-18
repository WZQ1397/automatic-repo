#!/bin/bash
echo -e "*******`date`*******" >> /var/log/rmbin.log
for file in `find /usr/local/mysql/var/* -path "/usr/local/mysql/var/mysql-bin.index" -prune -o -name "mysql-bin.*" -ctime +3 -print` 
do
	rm -rvf $file >> /var/log/rmbin.log
done

