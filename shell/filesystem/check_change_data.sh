#/bin/bash

# Check whether a file is unauthorized modification 
# If the file has been modified, note to log

#HOW TO
#0 3 * * * root check_change_data.sh /data/wwwroot/aaa.com
 
#Definition of variables
webmail=root

#vars!
website=$1

fingerbackup=/backup/Fingerprint
createlog=$fingerbackup/create.log
checklog=$fingerbackup/check.log
fingerfile=$fingerbackup/$(date +%F).Fingerprint
ofingerfile=$fingerbackup/$(date -d"1 day ago" +%F).Fingerprint

#Judge the backup directory exists
[ ! -d $fingerbackup ] && mkdir -p $fingerbackup

#Judge the MD5 exists
[ ! -f $fingerfile ] && find $website -type f | xargs md5sum > $fingerfile

#The file was modified
[ ! -f $checklog ] && touch $checklog
md5sum -c $fingerfile | grep -i "FAILED" > $checklog
md5sum -c $ofingerfile | grep -i "FAILED" | egrep -v "sitemap.xml.gz|sitemap.xml" > $checklog

:<<BLOCK
if [ `cat $checklog | wc -l` -gt 0 ];then
    mail -s "The file was modified" $webmail < $checklog
fi
BLOCK

#New file creation
[ ! -f $createlog ] && touch $createlog
if [ `ls -l --full-time $website | grep $(date +%F) | awk -F ' ' '{print $9}' | grep -v "^$" | wc -l` -gt 0 ];then
    echo "`ls -l --full-time $website | grep $(date +%F) | awk -F ' ' '{print $9}'`" > $createlog
else
    > $createlog
fi

:<<BLOCK
if [ `cat $createlog | grep -v "^$" | wc -l` -gt 0 ];then
    #echo `cat $errorlog`
    mail -s "New file creation" $webmail < $createlog
    > /backup/Fingerprint/create.log
fi
BLOCK