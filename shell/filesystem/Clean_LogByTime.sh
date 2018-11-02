#!/bin/bash
# Usage Clean_Log.sh PATH TIME
DAYS=$2
CLEAN_PATH=$1

cd $CLEAN_PATH
if [[ `pwd` == $CLEAN_PATH && $DAYS -ge 3 ]];
then
  find -ctime +$DAYS | xargs rm -rf \{};
  echo $CLEAN_PATH "CLEAN SUCCESS!" date >> /tmp/zach_clean.log
else
  echo $CLEAN_PATH "CLEAN failed!" date >> /tmp/zach_clean.log
fi
echo "+++++++++++++++++++++++" >> /tmp/zach_clean.log
sleep 30
> catalina.out

function printLine() {
        pri=`cat $1 | head -n$2 | tail -1f`
        #字符串长度是否为0,不为0输出
        if [ -n "${pri}" ]
        then
                echo ${pri}             
        fi
}

file1=./priip
file2=./pubip
file3=./type
num=`wc -l type | cut -d " " -f 1`

i=1
while (( i <= ${num} ))
do
        printLine ${file1} ${i}
        printLine ${file2} ${i}
        printLine ${file3} ${i}

        let i++
done