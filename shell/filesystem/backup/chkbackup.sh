#!/bin/sh
#检查备份目录下文件变化
log_file=chkresult-$(date +"%Y-%m-%d").log
echo "check result on $(date +'%Y-%m-%d'):" > $log_file
for file in $(find -maxdepth 2 -type d -name "$(date +'%Y%m')*" -o -name "$(date +'%y-%m')*" | grep -v 76200)
do
	echo "checking $file"
	idcount="$(ls -l $file | wc -l)"
	ispace="$(du $file -sh | cut -f 1)"
	printf "%s\t%s\t%s\n" $file $idcount $ispace >> $log_file
done
echo "check done" >> $log_file

