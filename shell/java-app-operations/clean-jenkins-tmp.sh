#!/bin/bash -x
com="sudo find /tmp/ -maxdepth 1 -name "grover*" -o -name "clover*" -o -name "sonar*" -o -name "npm*" -o -name "seleniumSslSupport*" -o -name "ssh*" -mtime +1  > /tmp/jes_cleanup_temp.txt"
whoami
hostname


eval $com

wc -l jes_cleanup_temp.txt

cd /tmp	
cat /tmp/jes_cleanup_temp.txt | while read line
do 
echo "INFO : deleting $line"
sudo rm -rf $line || true
done 

echo "I'm Done"